import { combineReducers } from 'redux';
import { test } from './test';

const appReducer = combineReducers({ test });

const rootReducer = (state, action) => {
    return appReducer(state, action);
};

export default rootReducer;
