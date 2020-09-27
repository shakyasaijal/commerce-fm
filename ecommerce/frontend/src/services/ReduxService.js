import { createStore, applyMiddleware, compose } from 'redux';
import { createLogger } from 'redux-logger';
import createSagaMiddleware from 'redux-saga';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

import rootReducer from '../reducers/root';
import { isProduction } from '../config/Config';
import rootSaga from '../sagas/root';

// Create Middleware
const SAGA_MIDDLEWARE = createSagaMiddleware();
const middlewares = [SAGA_MIDDLEWARE];

// Logger
const LOGGER = createLogger({
	collapsed: true,
});
// Enable redux logger in local and dev only
if (!isProduction()) {
	composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
	middlewares.push(LOGGER);
}

let composeEnhancers = compose;

// Persist
const persistWhitelist = [];
const persistConfig = {
	key: 'root',
	storage,
	whiteList: persistWhitelist,
};
const reduxPersistReducer = persistReducer(persistConfig, rootReducer);
const STORE = createStore(
	reduxPersistReducer,
	composeEnhancers(applyMiddleware(...middlewares))
);

export const runMiddlewares = (callback) => {
	persistStore(STORE, null, () => {
		SAGA_MIDDLEWARE.run(rootSaga);
		callback();
	});
};

export const getStore = () => {
	return STORE;
};

export const getState = () => {
	return STORE.getState();
};
