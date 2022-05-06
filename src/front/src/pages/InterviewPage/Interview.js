import './Interview.css';

import React, {useState, useEffect} from "react"; 
import firstVideo from "./interviewer_01.mp4";
// import secondVideo from "./interviewer_02.mp4";
import { Link } from 'react-router-dom';
let count = 1;

function Interview() {
    const [buttonState, setButtonState] = useState(true);
    const [questionNumberState, setQuestionNumberState] = useState(1);

    // function changeButtonStateTrue() {
    //     setButtonState(true);
    //     count+=1;
    // }
    // function changeButtonStateFalse() {
    //     setButtonState(false);
    //     setInterviewState(interviewState + 1);
    // }

    // useEffect(() => {
    //     console.log('count ', count);
    // }, [count]);

    // function changeQuestionNumberState() {
    //     setQuestionNumberState(questionNumberState + 1);
    // }

    return (
        <div className="interview-app">
            {/*------------------ 가상 면접관 ------------------*/}
            <div className="interviewer-section">
                <video width="100%" height="100%">
                    {/* <source src="./test_video.mp4" type="video/mp4">
                    </source> */}
                    <source src={firstVideo}/>
                </video>                
            </div>
            {/*-------------------- 사용자 --------------------*/}
            <div className="button-section">
                {/* state true : 면접 시작 button */}
                {buttonState 
                && <button className="interview-button" onClick={() => setButtonState(false)}>
                    면접 시작
                </button>}
                {/* state false : 다음 질문 button */}
                {!buttonState 
                && questionNumberState < 2 
                && <button className="done-button" onClick={() => setQuestionNumberState(questionNumberState + 1)}>
                    대답 완료
                </button>}
                {/* state false : 면접 종료 button */}
                {questionNumberState === 2 
                && <button className="interview-button">
                    <Link to="/mypage" className="link-to-mypage">
                        면접 종료
                    </Link>
                </button>}
            </div>
        </div>
    );
}


export default Interview;