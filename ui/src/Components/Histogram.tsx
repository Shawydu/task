import { Component } from 'react';
import { Chart } from 'react-google-charts';


type MyProps = {
    name: string,
    startLoading: boolean, // flag where parent component tells histogram file uploaded success, trigger the histogram pulling data
    handleUploadState: Function,
}

type MyState = {
    data: any,
    // ws: WebSocket | null,
}

interface CalculateData {
    columns: Array<string>,
    data: Array<any>,
    index: Array<number>,
}

class Histogram extends Component<MyProps, MyState> {
    ws!: WebSocket;
    timerId!: any;
    constructor(props: any) {
        super(props);

        this.state = {
            data: null,
        }
    }

    // setup web socket connection on component mount
    componentDidMount() {
        this.ws = new WebSocket(`ws://${process.env.REACT_APP_SERVER_HOST}${process.env.REACT_APP_API_V1}/${process.env.REACT_APP_GET_DATA}/${this.props.name}`);
        this.timerId = setInterval(
            () => this.retrieveData(),
            2000
        );
    }

    // close web socket connection on component unmount
    componentWillUnmount() {
        if(this.ws != null) {
            this.ws.close();
        }

    }

    retrieveData = () => {
        if(!this.props.startLoading || this.ws == null) {
            return;
        }

        this.ws.send("hello!");
        this.ws.onmessage = (event) => {
            const resp: CalculateData = JSON.parse(event.data);
            let expected_data = new Array(resp.columns);
            expected_data = expected_data.concat(resp.data);
            this.setState({
                data: expected_data
            });

            this.props.handleUploadState(false, this.props.name);
        }
    }

    render() {
        const { data } = this.state;
        return (
            <div className="container">
                { data != null && <Chart chartType="ColumnChart" width="100%" height="400px" data={data} />}
            </div>
        );
    }
}

export default Histogram;
