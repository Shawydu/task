import React from 'react'
import App from './App';
import Upload from './Components/Upload'
import Histogram from 'Components/Histogram';
import { shallow } from 'enzyme'

describe('Main App Component', () => {
    let wrapper: any;
    beforeEach(() => wrapper = shallow(
        <App />
    ))

    it('renders one upload and two histogram components correctly', () => {
        expect(wrapper.find(Upload).length).toBe(1);
        expect(wrapper.find(Histogram).length).toBe(2);
        expect(wrapper.state())
    });

    it('initializes states', () => {
        expect(wrapper.state('uploadSuccess')).toBeFalsy();
        expect(wrapper.state('inProgress').length).toBe(0);
    });

    it('handles upload state with true from initial states', () => {
        wrapper.instance().handleUploadState(true);
        expect(wrapper.state('uploadSuccess')).toBeTruthy();
        expect(wrapper.state('inProgress').length).toBe(2);
    });

    it('handles upload state with false from initial states', () => {
        wrapper.instance().handleUploadState(false);
        // states won't change
        expect(wrapper.state('uploadSuccess')).toBeFalsy();
        expect(wrapper.state('inProgress').length).toBe(0);
    });

    it('update upload state after uploading file success', () => {
        // mock upload success
        wrapper.instance().handleUploadState(true);
        
        // task 1 completes
        wrapper.instance().handleUploadState(false, '1');
        expect(wrapper.state('uploadSuccess')).toBeTruthy();
        expect(wrapper.state('inProgress').length).toBe(1);

        // task 2 completes, states changed back to initial states, as both tasks complete
        wrapper.instance().handleUploadState(false, '2');
        expect(wrapper.state('uploadSuccess')).toBeFalsy();
        expect(wrapper.state('inProgress').length).toBe(0);
    });
});
