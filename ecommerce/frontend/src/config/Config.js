export const getEnv = () => {
	return process.env.REACT_APP_ENV || 'local';
};

export const getEndPoint = () => {
	return process.env.REACT_APP_API_URL;
};

export const isProduction = () => {
	const env = getEnv().toLowerCase();
	return env === 'prod' || env === 'production';
};

export const getImageBasePath = (fileName) => {
	return getEndPoint() + fileName;
};
