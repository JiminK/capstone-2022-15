// import Button from ''
import './PreInterview.css';
import img_logo_long from './img_logo_long.png';
import { PageDescription } from '../../components/PageDescription';
import BT_mypage from './BT_mypage.png';
import img_logo_footer from './img_logo_footer.png';

import React, { Component } from "react"; 
import { Link } from 'react-router-dom';


class PreInterview extends Component {
    render() {
        return (
            <div className="PreInterviewApp">
                {/* <Header></Header> */}
                <PageDescription></PageDescription>
                <CamSetting></CamSetting>
                {/* <Footer_gray></Footer_gray> */}
            </div>
        );
    }
}


class CamSetting extends Component { 
    render() {
        return (
            <div className="cam-setting-layout">
                <span className="cam-setting-title">
                    WEBCAM 연결 · · ·
                </span>
                <div className="cam-show-layout">
                    <div className="cam-show">

                    </div>
                    {/* conneting webcam */}
                </div>
                <button className="start-button">
                    START
                </button>
            </div>
        );
    }
    

}


export default PreInterview;
