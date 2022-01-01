import React from 'react';
import './App.css';
import UploadFiles from './Components/Upload';
import Histogram from 'Components/Histogram';

type State = {
  uploadSuccess: boolean,
}

class App extends React.Component<{}, State> {
  constructor(props: any) {
    super(props);
    this.state = {
      uploadSuccess: false
    }
  }

  handleUploadState = (success: boolean) => {
    this.setState({
      uploadSuccess: success
    })
  }

  render() {
    const { uploadSuccess } = this.state;
    return (
      <div className="Container">
        <div className="row justify-content-center">
          <div className="col-md-4">
            <UploadFiles handleUploadState={this.handleUploadState}/>
          </div>
        </div>
        <div className="row">
          <Histogram name="1" startLoading={uploadSuccess} handleUploadState={this.handleUploadState}/>
        </div>
        <div className="row">
          <Histogram name="2" startLoading={uploadSuccess} handleUploadState={this.handleUploadState}/>
        </div>
      </div>
    );
  }
}

export default App;
