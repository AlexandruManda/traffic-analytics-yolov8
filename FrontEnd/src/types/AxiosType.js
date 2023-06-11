import axios from 'axios';

const URL = "http://localhost:5000/api";
let axiosForm =   axios.create({
  baseURL: URL,
  headers: {
    "Content-type": "multipart/form-data",
  }
});

const axiosInstance = axios.create({
  baseURL: URL,
});

const Axios = {
  axiosForm,
  axiosInstance
};
export default Axios;