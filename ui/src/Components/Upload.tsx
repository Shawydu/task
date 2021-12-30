import { Component } from 'react';
import axios from 'axios';
import './Upload.css'

type Props = {
  handleUploadState: Function
}

type UploadButtonState = {
  uploadFile: Blob,
  message : string
}

class UploadButton extends Component<Props, UploadButtonState> {
  constructor(props: any) {
    super(props);
    this.state = {
      uploadFile: new Blob(),
      message: ''
    };

  };

  onFileChange = (event: any) => {
    console.log(event.target.files[0]);
    this.setState({
      uploadFile: event.target.files[0]
    })
  };

  uploadFile = () => {
    if(this.state.uploadFile.size == 0) {
      this.setState({
        message: 'please upload/drop file first!'
      });
      return;
    }
    const data = new FormData();
    data.append('file', this.state.uploadFile);
    axios.post('http://localhost:8000/tasks/uploaddata', data, {
    }).then(resp => {
      this.setState({
        message: resp.data.message
      });

      this.props.handleUploadState(true);
    }).catch(err => {
      this.setState({
        message: err.response.data.detail
      });
    })
  };

  render() {
    const { message } = this.state;
    return (
      <div className="UploadFiles">
        <header className="App-header">
          <label className="form-label" htmlFor="customFile">Import data</label>
          <input type="file" className="form-control" id="customFile" onChange={this.onFileChange} />
          <button type="button" className="btn btn-success upload-btn" onClick={this.uploadFile}>Upload!</button>
        </header>
        { message != '' && <div className="message">
            {message}
          </div>
        }
      </div>
    )
  };
}

export default UploadButton;
