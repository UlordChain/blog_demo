<template>
<div>
  <div class="breadcrumbs">
    <div class="container">
      <h1 class="pull-left">搜索</h1>
      <ul class="pull-right breadcrumb">
      <li>
        <router-link to='/' class="turn">主页</router-link>
      </li>
      <span class="actived">/</span>
      <li class="ac">
        搜索结果
      </li>
    </ul>
    </div>
  </div>
<div class="container content">
    
    <div class="row">
      <div class="col-md-8 col-md-offset-2">
        <div class="error-v1">
        <span>哎呀!</span>
        <br>
        <p>您输入的</p><pre>{{msg}}</pre>未找到相关信息<br><br> <p></p>
        <a class="btn-u btn-bordered" href="/">回主页</a>
        </div>
      </div>
    </div>
  </div>
</div>
  
</template>
<script>
export default {
  name: "search",
  data() {
    return {
      msg: ""
    };
  },
  mounted() {
    this.msg = this.$route.query.q;
  }
};
</script>
<style lang="scss" scoped>
.content {
  padding-top: 40px;
  padding-bottom: 40px;
}
.error-v1 {
  padding-bottom: 30px;
  text-align: center;
}
.error-v1 span {
  color: #555;
  display: block;
  font-size: 35px;
  font-weight: 200;
}
.error-v1 p {
  color: #555;
  font-size: 16px;
}
pre {
  overflow: auto;
}
ode,
kbd,
pre,
samp {
  font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
}
pre {
  display: block;
  padding: 9.5px;
  margin: 0 0 10px;
  font-size: 13px;
  line-height: 1.42857143;
  color: #333;
  word-break: break-all;
  word-wrap: break-word;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.btn-u {
  border: 0;
  color: #fff;
  cursor: pointer;
  padding: 6px 13px;
  background: #3498db;
  white-space: nowrap;
}
.btn-u,
.list-toggle:after {
  font-size: 14px;
  display: inline-block;
  font-weight: 400;
  &:hover {
    background: #2980b9;
    color: #fff;
  }
}
</style>

