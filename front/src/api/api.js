import request from '@/utils/request'

export function getAbi(contractName) {
  return request({
    url: "/get/abi/" + contractName,
    method: 'get'
  })
}

export function login(username, password) {
  console.log(this);
  return request({
    url: "/post/user/login",
    method: 'post',
    data: {
      username,
      password,
      "address": this.$web3.eth.defaultAccount
    }
  })
}

export function register(username, password) {
  return request({
    url: "/post/user/register",
    method: 'post',
    data: {
      username,
      password,
      "address": this.$web3.eth.defaultAccount
    }
  })
}