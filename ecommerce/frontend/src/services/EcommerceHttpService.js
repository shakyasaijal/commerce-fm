import { httpService } from '../services/HttpService';

const getMethod = 'get';

class EcommerceHttpService {
    async getAuthorizationHeaders() {
        return {
            Authorization: '',
        };
    }

    async get(path, query = null) {
        const headers = await this.getAuthorizationHeaders();
        return httpService.request(getMethod, headers, path, query);
    }
}
const ecommerceHttpService = new EcommerceHttpService();

export default ecommerceHttpService;
