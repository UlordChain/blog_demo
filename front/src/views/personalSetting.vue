<template>
  <div class="settingContainer">
    <div class="settingItem clearfix">
      <div class="setting-label">手机号码</div>
      <div class="setting-status">{{username | usernameTrans}}</div>
      <!-- <div class="setting-bind">绑定</div> -->
    </div>
    <div class="settingItem clearfix">
      <div class="setting-label">登录密码</div>
      <div class="setting-status">********</div>
      <router-link to="/personal/newPassword" class="setting-bind">修改</router-link>
    </div>
    <div class="settingItem clearfix">
      <div class="setting-label">实名认证</div>
      <div class="setting-status" v-if="!real">未认证</div>
      <div class="setting-status" v-if="real">已认证</div>
      <router-link to="/personal/realNameAuth" class="setting-bind">认证</router-link>
    </div>
    <!-- <div class="settingItem clearfix">
        <div class="setting-label">Github账号</div>
        <div class="setting-status">未绑定</div>
        <div class="setting-bind">绑定</div>
    </div>
    <div class="settingItem clearfix">
      <div class="setting-label">钱包地址</div>
      <div class="setting-status">未绑定</div>
      <div class="setting-bind">绑定</div>
    </div> -->
    </div>
</template>
<script>
import store from '../store'
export default {
  data() {
      return {
        real: store.getters.real,
        username: store.getters.name
      }
  },
  filters: {
    usernameTrans(value) {
      return String(value).substr(0, 3) + '****' + String(value).substr(7);
    }
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  },
  mounted() {
  }
}

</script>

<style lang="scss" scoped>
.settingContainer {
    padding: 30px 25px;
}
.settingContainer .settingItem {
    border-bottom: 1px solid #eee;
    line-height: 66px;
    padding: 0px 25px;
    position: relative;
    box-sizing: border-box;
    width: 100%;
}

.settingContainer .settingItem .setting-label {
    font-size: 14px;
    color: #999999;
    width: 110px;
    float: left;
}

.settingContainer .settingItem .setting-status {
    float: left;
    font-size: 14px;
    color: #666666;
}

.settingContainer .settingItem .setting-bind {
    float: right;
    line-height: 66px;
    font-size: 14px;
    color: #4F81F4;
    cursor: pointer;
}
.clearfix::before,
.clearfix::after {
    content: '';
    display: block;
}

.clearfix::after {
    clear: both;
}
</style>
