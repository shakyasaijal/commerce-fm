import * as allTypes from '../actions/types';

const initialState = {};

export const test = (state = initialState, action) => {
	switch (action.type) {
		case allTypes.GET_SYS_INFO: {
			return { ...state };
		}
		default:
			return state;
	}
};
