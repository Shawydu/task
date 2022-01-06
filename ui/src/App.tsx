import React from 'react';
import './App.css';
import FileUpload from './Components/Upload';
import Histogram from 'Components/Histogram';

type State = {
  uploadSuccess: boolean, // flag pops up from upload, mark file upload success/fail
  inProgress: Array<string>, // record the number of histogram component under ticking of retrieving data
}

class App extends React.Component<{}, State> {
  constructor(props: any) {
    super(props);
    this.state = {
      uploadSuccess: false,
      inProgress: new Array(),
    }
  }

  /***
   *  this method is for child componentd control the state so that upload and histogram can talk to each other
   *  1. state == true: invoked by upload component, indicating that upload success
   *  2. state == false: invoked by histogram component, indicating that data retrieved success
   * 
   *  we set inProgress with 2 tasks on upload success, remove task from bucket once histogram component invokes it.
   *  "uploadSuccess" marked as true until the task bucket size is 0.
   * */ 
  handleUploadState = (state: boolean, task: string) => {
    let inProgress = this.state.inProgress;
    if(state) {
      inProgress.push('1', '2');
    } else {
      inProgress = inProgress.filter(e => e !== task);
    }

    this.setState({
      uploadSuccess: inProgress.length > 0 || state,
      inProgress: inProgress,
    });
  }

  render() {
    const { uploadSuccess} = this.state;
    return (
      <div className="Container">
        <div className="row justify-content-center">
          <div className="col-md-4">
            <FileUpload handleUploadState={this.handleUploadState}/>
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
