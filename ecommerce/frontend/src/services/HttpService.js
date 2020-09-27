import Axios from 'axios';

const COMMON_HEADERS = {
	Accept: 'application/json',
	'Content-Type': 'application/json',
};

class HttpService {
	validateResponse(response) {
		if (response.status === 401) {
			window.stop();
			// Any operations eg. force logout, error display, etc.
		}
		return response;
	}

	async request(method = 'get', header, url, query = null, data = null) {
		let options = {};
		let headers = { ...COMMON_HEADERS, ...header };
		if (method === 'post') headers = { ...header };

		try {
			options = { url, method, headers };
			if (data) {
				options.body = data;
			}
		} catch (e) {
			const errPayload = {
				method,
				url,
				query,
				data,
			};
			console.log('services/HttpService: ', errPayload, e);
			return e;
		}
		try {
			const response = await Axios(options);
			if (response.data.status) {
				this.validateResponse(response);
			}
			return response;
		} catch (e) {
			const errPayload = [method, url, headers];
			console.log('Network Error: ', errPayload, e);
			return e;
		}
	}
}

export const httpService = new HttpService();
