

export function isvalidUsername(str) {
  const phoneregex = /^[1][3,4,5,7,8][0-9]{9}$/
  return phoneregex.test(str)
}

export function userName(str) {
  const re = /^[\u4E00-\u9FA5A-Za-z0-9]+$/
  return re.test(str);
}
/* 合法uri*/
// export function validateURL(textval) {
//   const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
//   return urlregex.test(textval)
// }

export function validateURL(textval) {
  const urlregex = /(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/
  return urlregex.test(textval)
}

/* 小写字母*/
export function validateLowerCase(str) {
  const reg = /^[a-z]+$/
  return reg.test(str)
}

/* 大写字母*/
export function validateUpperCase(str) {
  const reg = /^[A-Z]+$/
  return reg.test(str)
}

/* 大小写字母*/
export function validatAlphabets(str) {
  const reg = /^[A-Za-z]+$/
  return reg.test(str)
}


export function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(email)
}

export function validateNickName(name) {
  const re = /^[a-zA-Z0-9\u4E00-\u9FA5]{2,10}$/
  return re.test(name);
}

export function validateNickName3(name) {
  const re = /^[a-zA-Z0-9\u4E00-\u9FA5]{1,30}$/
  return re.test(name);
}

export function validateMainName(name) {
  const re = /^[a-zA-Z0-9_-]{2,10}$/
  return re.test(name);
}

export function validateMainName2(name) {
  const re = /^[a-zA-Z0-9_-]{1,19}$/
  return re.test(name);
}

export function validateCard(value) {
  const re =  /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
  return re.test(value)
}

export function txId(value) {
  const re = /^[a-zA-Z0-9_]+$/
  return re.test(value);
}

export function ip(value) {
  const re = /^(127\.0\.0\.1)|(localhost)|(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|(172\.((1[6-9])|(2\d)|(3[01]))\.\d{1,3}\.\d{1,3})|(192\.168\.\d{1,3}\.\d{1,3})$/
  return re.test(value);
}


