import React, { Component } from "react"
import { intlShape } from "react-intl"
import PropTypes from "prop-types"
import validator from 'validator'
import { v4 } from "uuid"

import ButtonCustomerEdit from "../../../components/ui/ButtonCustomerEdit"


class CustomerDisplay extends Component {
    constructor(props) {
        super(props)
        console.log("Customer display props:")
        console.log(props)
        this.videoStream = React.createRef()
        this.snap = React.createRef()
        this.superSecretPictureCanvas = React.createRef()
    }

    PropTypes = {
        intl: intlShape.isRequired,
        customerID: PropTypes.integer,
        customers: PropTypes.object,
        edit_in_progress: PropTypes.boolean,
        onClickEdit: PropTypes.function
    }


    onClickStartCamera() {
        console.log('Home component DidMount')
        // var constraints = { audio: false, video: { facingMode: 'user' } }
        if (navigator.mediaDevices.getUserMedia) {       
            navigator.mediaDevices.getUserMedia({video: true})
          .then(stream => {
            this.videoStream.current.srcObject = stream
          })
          .catch(error => {
            console.log("Something went wrong while trying to stream video!");
            console.log(error)
          });
        }
        
    }

    onClickTakePhoto() {
        console.log('say cheese!!')
        var snap = this.takeSnapshot();

        // Show image. 
        this.snap.current.setAttribute('src', snap);
        // image.classList.add("visible");

        // Enable delete and save buttons
        // delete_photo_btn.classList.remove("disabled")
        // download_photo_btn.classList.remove("disabled")

        // Set the href attribute of the download button to the snap url.
        // download_photo_btn.href = snap

        // Pause video playback of stream.
        this.videoStream.current.pause()
    }


    takeSnapshot(){
        // Here we're using a trick that involves a hidden canvas element.  
        var video = this.videoStream.current
        var hidden_canvas = this.superSecretPictureCanvas.current
        var context = hidden_canvas.getContext('2d');

        var width = video.videoWidth
        var height = video.videoHeight

        if (width && height) {

            // Setup a canvas with the same dimensions as the video.
            hidden_canvas.width = width;
            hidden_canvas.height = height;

            // Make a copy of the current frame in the video on the canvas.
            context.drawImage(video, 0, 0, width, height);

            // Turn the canvas image into a dataURL that can be used as a src for our photo.
            return hidden_canvas.toDataURL('image/png');
        }
    }


    render() {
        const customerID = this.props.customerID
        const customers = this.props.customers
        const edit_in_progress = this.props.edit_in_progress
        const onClickEdit = this.props.onClickEdit

        return (
            <div>
                { !(customerID) || (edit_in_progress) ? null :
                <div className="box box-solid"> 
                    <div className="box-header">
                        <h3 className="box-title">Customer</h3>
                    </div>
                    <div className="box-body">
                        <div className="col-md-6">
                            <div className="camera-app">
                                <button id="start-camera" 
                                        className="visible"
                                        onClick={this.onClickStartCamera.bind(this)} >
                                    Start camera
                                </button>
                                <video id="camera-stream" 
                                    autoPlay 
                                    ref={this.videoStream}></video>
                                <img ref={this.snap} id="snap" />

                                <p id="error-message"></p>

                                <div className="controls">
                                    <button id="delete-photo" title="Delete Photo" className="disabled"><i className="fa fa-ban"></i></button>
                                    <button id="take-photo" onClick={this.onClickTakePhoto.bind(this)} title="Take Photo"><i className="fa fa-camera"></i></button>
                                    <button id="download-photo" download="selfie.png" title="Save Photo" className="disabled"><i className="fa fa-save"></i></button>  
                                </div>

                                {/* <!-- Hidden canvas element. Used for taking snapshot of video. --> */}
                                <canvas ref={this.superSecretPictureCanvas}></canvas>
                            </div>
                        </div>
                        <div className="col-md-6">
                            {customers[customerID].display_name}
                            {customers[customerID].address}
                            <ButtonCustomerEdit onClick={onClickEdit}/>
                        </div>
                    </div>
                </div>
                }
            </div>
        )
    }
}

export default CustomerDisplay

