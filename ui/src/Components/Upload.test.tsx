import React from 'react';
import FileUpload from './Upload';
import { shallow } from 'enzyme'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter';

describe('Upload Component', () => {
    let wrapper : any;
    const handleUploadState = jest.fn();
    beforeEach(() => wrapper = shallow(
        <FileUpload handleUploadState={handleUploadState} />
    ));

    it('renders dom correctly', () => {
        expect(wrapper.find('input#customFile').length).toBe(1);
        expect(wrapper.find('button').length).toBe(1);
    });

    it('initializes states correctly', () => {
        expect(wrapper.state('uploadFile')).toBeTruthy();
        expect(wrapper.state('message').length).toBe(0);
    });

    it('upload a file and set to state', () => {
        const file = 'dummyValue.something'
        wrapper.find('input#customFile').simulate('change', {
            target: {
                files: [
                    file
                ]   
            }
        });

        expect(wrapper.state('uploadFile')).toBe(file);
    });

    it('clicks upload button withoout putting any file', () => {
        const messageDomTag = 'div.message';
        expect(wrapper.find(messageDomTag).length).toBe(0);
        wrapper.find('button').simulate('click');
        expect(wrapper.state('message')).toBe('please upload/drop file first!');
        expect(wrapper.find(messageDomTag).length).toBe(1);
    });

    jest.mock('axios');

    // it('uploads file successfully', () => {
    //     const file = 'dummyValue.something'
    //     wrapper.find('input#customFile').simulate('change', {
    //         target: {
    //             files: [
    //                 file
    //             ]   
    //         }
    //     });
    //     axios.post.mockImplementation(() => Promise.resolve({}));


    // });
});

describe('Upload API interactions', () => {
    let wrapper : any;
    const handleUploadState = jest.fn();
    let mockAxios : any;
    const mockHandleUploadStateFunc = jest.fn();
    beforeEach(() => {
        wrapper = shallow(
            <FileUpload handleUploadState={handleUploadState} />
        );
        wrapper.setState({ uploadFile: 'dummyValue.something'});
        wrapper.setProps({ handleUploadState: mockHandleUploadStateFunc});
        mockAxios = new MockAdapter(axios);
    });

    it('uploads file successfully', (done) => {
        const messageDomTag = 'div.message';
        expect(wrapper.find(messageDomTag).length).toBe(0);
        const expectedMessage = 'upload successfully!';
        mockAxios.onPost(`http://${process.env.REACT_APP_SERVER_HOST}${process.env.REACT_APP_API_V1}/${process.env.REACT_APP_UPLOAD_ENDPOINT}`).reply(202, {
            message: expectedMessage
        });
        wrapper.find('button').simulate('click');
        
        setTimeout(() => {
            expect(wrapper.state('message')).toBe(expectedMessage);
            expect(mockHandleUploadStateFunc).toHaveBeenCalledTimes(1);
            expect(mockHandleUploadStateFunc).toBeCalledWith(true);
            expect(wrapper.find(messageDomTag).length).toBe(1);
            done();
        });
    });

    it('uploads a bad file', (done) => {
        const messageDomTag = 'div.message';
        expect(wrapper.find(messageDomTag).length).toBe(0);
        const expectedMessage = 'invalid file!';
        mockAxios.onPost(`http://${process.env.REACT_APP_SERVER_HOST}${process.env.REACT_APP_API_V1}/${process.env.REACT_APP_UPLOAD_ENDPOINT}`).reply(400, {
            message: expectedMessage
        });
        wrapper.find('button').simulate('click');
        
        setTimeout(() => {
            expect(wrapper.state('message')).toBe(expectedMessage);
            expect(mockHandleUploadStateFunc).toHaveBeenCalledTimes(0);
            expect(wrapper.find(messageDomTag).length).toBe(1);
            done();
        });
    });
});
