import { GET_SYS_INFO } from '../actions/types';
import { takeLatest, all } from 'redux-saga/effects';

function* handleTestRequest() {
	//   const { callBackSuccess, callBackError } = action;
}

function* watchTest() {
	yield takeLatest(GET_SYS_INFO, handleTestRequest);
}

export default function* testSaga() {
	yield all([watchTest()]);
}
