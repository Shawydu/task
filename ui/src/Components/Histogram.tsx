import { Component } from 'react';
import { Chart } from 'react-google-charts';

type MyProps = {
    name: string,
    startLoading: boolean,
    handleUploadState: Function,
}

type MyState = {
    data: any,
    readyState: boolean,
}

interface CalculateData {
    columns: Array<string>,
    data: Array<any>,
    index: Array<number>,
}

class Histogram extends Component<MyProps, MyState> {
    constructor(props: any) {
        super(props);

        this.state = {
            data: null,
            readyState: false,
        }
    }

    retrieveData = () => {
        if(this.state.readyState || !this.props.startLoading) {
            return;
        }

        const ws = new WebSocket("ws://localhost:8000/tasks/" + this.props.name);
        ws.onmessage = (event) => {
            const resp: CalculateData = JSON.parse(event.data);
            let expected_data = new Array(resp.columns);
            expected_data = expected_data.concat(resp.data);
            this.setState({
                data: expected_data
            });

            this.props.handleUploadState(false);
            this.setState({
                readyState: true
            })
        }
    }

    render() {
        this.retrieveData();
        const { data } = this.state;
        return (
            <div className="container">
                { data != null && <Chart chartType="ColumnChart" width="100%" height="400px" data={data} />}
            </div>
        );
    }
}

export default Histogram;
