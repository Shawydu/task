import React from 'react';
import Histogram from './Histogram';
import { shallow } from 'enzyme';
import WS from 'jest-websocket-mock';

describe('Histogram Component', () => {
    let wrapper : any;
    const handleUploadState = jest.fn();
    const taskName = 'genius';
    
    beforeEach(() => wrapper = shallow(
        <Histogram handleUploadState={handleUploadState} name={taskName} startLoading={false} />
    ));

    it('renders dom and initializes states correctly', () => {
        expect(wrapper.find('div.container').length).toBe(1);
        // it start with an empty container
        expect(wrapper.find('Chart').length).toBe(0);
        expect(wrapper.state('data'))
    });

    it('initializes states correctly', () => {
        const instance = wrapper.instance();
        
        expect(instance.ws).toBeTruthy();
        expect(instance.ws.url).toContain(taskName);
        expect(instance.timerId).toBeTruthy();
    });
});

describe('retrieve data over web socket', () => {let wrapper : any;
    const handleUploadState = jest.fn();
    const taskName = 'genius';
    // use this third party library to mock a web socket server, to interact with our client
    const mockServer = new WS(`ws://${process.env.REACT_APP_SERVER_HOST}${process.env.REACT_APP_API_V1}/${process.env.REACT_APP_GET_DATA}/${taskName}`);
    
    beforeEach(() => {
        wrapper = shallow(
            <Histogram handleUploadState={handleUploadState} name={taskName} startLoading={false} />
        )
        wrapper.setProps({ startLoading: true});
    });

    it('sends text over web socket', async () => {
        await mockServer.connected;
        wrapper.instance().retrieveData();

        await expect(mockServer).toReceiveMessage("hello!");
    });

    it('retrieves data from server, renders histogram', async () => {
        await mockServer.connected;
        const mockResp = "{\n            \"index\": [\n                0,\n                1,\n                2,\n                3,\n                4\n            ],\n            \"columns\": [\n                \"education\",\n                \"percentage\"\n            ],\n            \"data\": [\n                [\n                    \"Bachelors\",\n                    0.4\n                ],\n                [\n                    \"HS-grad\",\n                    0.2\n                ],\n                [\n                    \"Masters\",\n                    0.2\n                ],\n                [\n                    \"11th\",\n                    0.1\n                ],\n                [\n                    \"9th\",\n                    0.1\n                ]\n            ]\n        }"
        mockServer.send(mockResp);

        expect(wrapper.state('data')).toBeTruthy();
        expect(wrapper.find('Chart').length).toBe(1);
    });

    it('gets network error from web socket', async () => {
        await mockServer.connected;
        const mockResp = "{\n            \"index\": [\n                0,\n                1,\n                2,\n                3,\n                4\n            ],\n            \"columns\": [\n                \"education\",\n                \"percentage\"\n            ],\n            \"data\": [\n                [\n                    \"Bachelors\",\n                    0.4\n                ],\n                [\n                    \"HS-grad\",\n                    0.2\n                ],\n                [\n                    \"Masters\",\n                    0.2\n                ],\n                [\n                    \"11th\",\n                    0.1\n                ],\n                [\n                    \"9th\",\n                    0.1\n                ]\n            ]\n        }"
        mockServer.send(mockResp);
        // it renders data successfully at first
        expect(wrapper.state('data')).toBeTruthy();
        expect(wrapper.find('Chart').length).toBe(1);

        // chart and data cleared once web socket hits error
        mockServer.error();
        expect(wrapper.state('data')).toBeFalsy();
        expect(wrapper.find('Chart').length).toBe(0);
    });
});
