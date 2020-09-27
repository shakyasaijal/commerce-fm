import React, { useEffect, useState } from 'react';
import ReactDom from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { Provider } from 'react-redux';

import PATHS from './routes';
import { runMiddlewares, getStore } from './services/ReduxService';
import Home from './Components/Home';

const DEFAULT_TITLE = 'E-Commerce';

const EcommerceRouter = (props) => {
	const { title, path, component } = props;
	document.title = title || DEFAULT_TITLE;
	window.scroll(0, 0);
	return <Route path={path} component={component} />;
};

const App = () => {
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		runMiddlewares(() => {
			setIsLoading(false);
		});
	}, []);

	if (isLoading) return <div className="App">Loading...</div>;
	const reduxStore = getStore();
	return (
		<Provider store={reduxStore}>
			<Router>
				<Switch>
					<EcommerceRouter exact path={PATHS.HOME} component={Home} />
					<EcommerceRouter exact path={PATHS.NOT_FOUND} component={Home} />
				</Switch>
			</Router>
		</Provider>
	);
};

ReactDom.render(<App />, document.getElementById('app'));
