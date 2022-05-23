import io

from django.contrib.auth import get_user_model, authenticate, login

from rest_framework import permissions, authentication

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import CreateUserSerializer, LoginUserSerializer
from rest_framework.authtoken.models import Token

from interview.models import Interview
from django.core import serializers
import numpy as np

# s3
import boto3
from .file_manage import select
s3 = boto3.resource('s3')
s3_interviewee = boto3.client('s3')


User = get_user_model()


class SignupView(APIView):
    http_method_names = ["post"]

    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, *args, **kwargs):
        serializer = CreateUserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            token = Token.objects.create(user=user)  # token create
            print(f'{user} signup success')
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "success": True,
                    "token": token.key,
                },
            )
        # already id exists etc..
        print(f'error: {serializer.errors}')
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "errors": serializer.errors,
            },
        )


class LoginView(APIView):
    authentication_classes=[
        authentication.TokenAuthentication
    ]

    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user_id = user_data["user_id"]
        password = user_data["password"]

        # wrong request
        if user_id is None or password is None:
            print("user id/pw required")
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"isLogin": False, "error": "user id/password required"},
            )
        user = User.objects.filter(user_id=user_id).first()
        # not founded user
        if user is None:
            print("user is not founded")
            return Response(
                {"isLogin": False, "error": "user is not founded"}, status=status.HTTP_404_NOT_FOUND
            )
        # wrong password
        if not user.check_password(password):
            print("wrong password")
            return Response(
                {"isLogin": False, "error": "wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )
        # success
        token = Token.objects.get(user=user)  # token get
        print("success login", user_id)
        return Response(
            status=status.HTTP_200_OK,
            data={"isLogin": True, "user_id": user_id, "token":token.key},
        )


class MypageView(APIView):
    permission_class=[
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        query = Interview.objects.filter(author_id=request.user)
        query_data = serializers.serialize('json', query)
        print(f"{request.user}: mypage success")
        return HttpResponse(query_data, content_type="text/json-comment-filtered")


class FeedbackView(APIView):
    permission_class=[
        permissions.IsAuthenticated
    ]

    def get(self, request, interview_id, question_n, *args, **kwargs):
        data = []

        # s3 presigned url
        bucket = 'user-feedback-bucket'

        key_list = select(request.user, interview_id, question_n)
        print(key_list)
        #key_list = select('haha', 2, 0)

        for (i, key) in zip(range(4), key_list):
            obj = s3.Object(bucket, key)
            body = obj.get()['Body'].read()

            time_min = 1
            time_max = 0

            # iris movement / volume interview
            if i == 0 or i == 1:
                with io.BytesIO(body) as f:
                    f.seek(0)
                    X, Y = np.load(f).values()
                
                d_ = []
                for j in range(0, len(X), 60):
                    d = dict()
                    d['name'] = np.round(X[j])
                    d['x'] = X[j]
                    d['y'] = Y[j]
                    time_min = min(time_min, X[j])
                    time_max = max(time_max, X[j])
                    d_.append(d)
                data.append(d_)
                #print(i, d_)
                #print()

            # face movement
            if i == 2:
                with io.BytesIO(body) as f:
                    f.seek(0)
                    XY = np.load(f).values()

                d_ = []
                time = np.linspace(time_min, time_max, len(d_))
                for j in range(0, len(XY), 60):
                    d = dict()
                    d['x'] = time[j]
                    d['y'] = XY[j]
                    d_.append(d)
                data.append(d_)
                # print(i, d_)
                # print()

            
            # stt interview
            if i == 3:
                with io.BytesIO(body) as f:
                    f.seek(0)
                    #txt = np.load(f).values()
                #data.append(txt)
                
        # presigned url 추가
        bucket = 'user-interview-video-bucket'
        key = 'user_id_{}/interview_id_{}/interview_video/interview_{}.mp4'.format(request.user, interview_id, question_n)
        interviewee_url = s3_interviewee.generate_presigned_url(ClientMethod='get_object',
                                                                Params={'Bucket': bucket, 'Key': key})

        return Response(status=status.HTTP_200_OK, data={
                                "face_movement": data[0],
                                "iris_movement": data[1],
                                "volume_interview": data[2],
                                "stt_interview": "123",
                                "interviewee_url": interviewee_url
        })

        """
        #user_id_rkawkaks/interview_id_1/result/volume_interview_0.npz
        user = 'rkawkaks'
        #user = 'yei'
        #interview_id = 1
        #question_n = 0

        key = f'user_id_{user}/interview_id_{interview_id}/result/volume_interview_{question_n}.npz'
        obj = s3.Object(bucket, key)

        body = obj.get()['Body'].read()
        with io.BytesIO(body) as f:
            f.seek(0)
            X, Y = np.load(f).values()

        key = f'user_id_{user}/interview_id_{interview_id}/result/stt_interview_.txt'
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read()


        data = []
        for i in range(0, len(X), 5):
            d = dict()
            d['name'] = str(round(X[i]))+'초'
            d['x'] = X[i]
            d['y'] = Y[i]
            data.append(d)

        user='yei'
        interview_id = 2
        question_n = 1
        bucket = 'user-interview-video-bucket'
        key = 'user_id_{}/interview_id_{}/interview_video/interview_{}.mp4'.format(user, interview_id, question_n)
        interviewee_url = s3_interviewee.generate_presigned_url(ClientMethod='get_object', Params={'Bucket':bucket, 'Key':key})

        print(f'{request.user}: feedback success')

        return Response(status=status.HTTP_200_OK, data={"success":True,
                                                        "volume_interview": data,
                                                        "stt_interview": body,
                                                        "interviewee_url": interviewee_url
                                                        })
        """
        #return HttpResponse(body, content_type="text/json-comment-filtered")



