<template>
  <div class="password-container">
    <el-form class="register-form" autoComplete="on" :model="registerForm" :rules="registerRules" ref="registerForm" label-position="left">
      <div class="login-nav">
        <h2>Ulord 社区开发者<span>通行证</span></h2>
        <div class='nav'>
          已有账号，
          <router-link to="/login" class='toLogin'>马上登录</router-link>
          <span class='divider'></span>
          <router-link to="/" class="return">返回首页</router-link>
        </div>
      </div>
      <h3 class="title">重置密码</h3>
      <el-form-item prop="username">
        <el-select v-model="registerForm.value" placeholder="请选择">
          <el-option v-for="item in options" :key="item.index" :value="'+'+item[2]" class="area">
          </el-option>
        </el-select>
        <el-input name="username" class="username" type="text" @input="checkNo(registerForm.username)"  v-model="registerForm.username" autoComplete="on" maxlength="11" placeholder="手机号" />
      </el-form-item>
      <div class="smcode-wrap">
        <el-form-item prop="smcode">
          <el-input name="smcode" class="smcode" type="tel" @input="checkNo2(registerForm.smcode)"  v-model="registerForm.smcode" autoComplete="off" maxlength="6" placeholder="验证码" />
        </el-form-item>
        <el-form-item prop="smcodeButton">
          <el-button type="primary" :disabled="codeDisabled" :loading="loadingSm" @click.native.prevent="sendCode"><span v-show="!show">发送验证码</span><span v-show="show">{{count}}秒</span></el-button>
        </el-form-item>
      </div>
      <el-form-item prop="password">
        <el-input name="password" type="password"  v-model="registerForm.password" autoComplete="on" maxlength="16" placeholder="请输入新密码"></el-input>
      </el-form-item>
       <el-form-item prop="confirmPassword">
        <el-input name="password" type="password"  v-model="registerForm.confirmPassword" autoComplete="on" maxlength="16" placeholder="请再次确认密码"></el-input><i v-if="isPassWord" class="password-icon"></i>
      </el-form-item>
      <el-form-item>
        <el-button v-bind:type="btn ? 'primary': 'info'" :disabled="!btn" style="width:100%;" :loading="loading" @click.native.prevent="handleRegister">
          确认重置
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getsmscode, resetPassword2 } from "@/api/api";
import { isvalidUsername, userName } from "@/utils/validate";
import allCountrys from "@/components/allCountrys";

export default {
  name: "register",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入手机号"));
      } else if (!isvalidUsername(value)) {
        callback(new Error("请输入正确的手机号"));
      } else {
        callback();
      }
    };
    const validateConfirmPassword = (rule, value, callback) => {
      if (value === "") {
        this.isPassWord = false;
        callback(new Error("请再次确认密码"));
      } else if (value !== this.registerForm.password) {
        this.isPassWord = false;
        callback(new Error("两次输入密码不一致!"));
      } else {
        this.isPassWord = true;
        callback();
      }
    };
    const validateCode = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入验证码"));
      } else {
        // else if (value) {
        //   smVerify(this.registerForm.username, parseInt(this.registerForm.value) ,value).then(res => {
        //     if (!res.data.success) {
        //       callback(new Error("请输入正确的验证码"));
        //     } else {
        //       callback();
        //     }
        //   });
        // }
        callback();
      }
    };
    const validatePass = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error("请输入8-16位数字、字母、字母区分大小写"));
      } else if (value.length > 16) {
        callback(new Error("请输入8-16位数字、字母、字母区分大小写"));
      } else {
        callback();
        this.$refs.registerForm.validateField('confirmPassword')
      }
    };
    return {
      options: allCountrys,
      isPassWord: false,
      registerForm: {
        username: "",
        password: "",
        confirmPassword: "",
        smcode: "",
        value: "+86"
      },
      registerRules: {
        username: [
          {
            required: true,
            trigger: "blur",
            validator: validateUsername
          }
        ],
        password: [
          {
            required: true,
            trigger: "blur",
            validator: validatePass
          }
        ],
        confirmPassword: [
          {
            required: true,
            trigger: "blur",
            validator: validateConfirmPassword
          }
        ],
        smcode: [
          {
            required: true,
            trigger: "blur",
            validator: validateCode
          }
        ]
      },
      dialogVisible: false,
      loadingSm: false,
      aab: false,
      loading: false,
      codeDisabled: false,
      codeLoading: false,
      count: "",
      timer: null,
      show: false
    };
  },
  computed: {
    btn: function() {
      return Boolean(
        this.registerForm.username &&
          this.registerForm.password &&
          this.registerForm.smcode &&
          this.registerForm.confirmPassword
      );
    }
  },
  methods: {
    checkNo(value) {
      if (value) {
        setTimeout(() => {
          this.registerForm.username = this.registerForm.username.replace(
            /\D/g,
            ""
          );
        }, 100);
      }
    },
    checkNo2(value) {
      if (value) {
        setTimeout(() => {
          this.registerForm.smcode = this.registerForm.smcode.replace(
            /\D/g,
            ""
          );
        }, 100);
      }
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true;
          resetPassword2(
            this.registerForm.username,
            this.registerForm.smcode,
            this.registerForm.password,
            parseInt(this.registerForm.value)
          )
            .then(res => {
              this.loading = false;
              if (res.data.errorCode == "OK") {
                this.$message({
                  message: "重置成功!",
                  type: "success"
                });
                this.$router.push({
                  path: "/login"
                });
              } else {
                this.$message({
                  message: "重置失败,请重试",
                  type: "error"
                });
              }
            })
            .catch(() => {
              this.loading = false;
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    sendCode() {
      this.$refs.registerForm.validateField("username", smcode => {
        if (smcode !== "") {
          return false;
        }
        this.loadingSm = true;
        getsmscode(
          this.registerForm.username,
          parseInt(this.registerForm.value)
        ).then(res => {
          const TIME_COUNT = 60;
          this.show = false;
          this.codeDisabled = true;
          this.loadingSm = false;
          if (!this.timer) {
            this.count = TIME_COUNT;
            this.codeDisabled = false;
            this.show = true;
            this.timer = setInterval(() => {
              if (this.count > 0 && this.count <= TIME_COUNT) {
                this.count--;
                this.show = true;
                this.codeDisabled = true;
              } else {
                this.show = false;
                clearInterval(this.timer);
                this.timer = null;
                this.codeDisabled = false;
              }
            }, 1000);
          }
        });
      });
    },
    handleClose(done) {
      done();
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss">
$bg: #f4f4f4;
$light_gray: #666;

/* reset element-ui css */

.password-container {
  .password-icon {
    position: absolute;
    bottom: 12px;
    display: inline-block;
    width: 20px;
    height: 20px;
    background: url(../assets/passwordpass.png) center center no-repeat;
  }
  .register-form {
    .el-form {
      background-color: #fff;
    }
    .el-form-item {
      margin: 0 auto 22px;
      width: 336px;
    }
    .el-select {
      width: 90px;
      font-size: 14px;
      color: #666666;
    }
    .el-icon-arrow-up:before {
      content: "\E60C";
    }
    .el-input {
      display: inline-block;
      width: 100%;
      input {
        -webkit-appearance: none;
        border-radius: 4px;
        color: $light_gray;
        background: #f4f4f4;
        border: 1px solid #dddddd;
        border-radius: 4px;
        &:-webkit-autofill {
          -webkit-box-shadow: 0 0 0px 1000px #f4f4f4 inset !important;
          -webkit-text-fill-color: #666666 !important;
        }
        &:focus {
          -webkit-box-shadow: 0 0 0px 1000px #f4f4f4 inset !important;
        }
      }
    }
    .el-form-item__content {
      line-height: 44px;
      position: relative;
      font-size: 14px;
    }
    .el-input__inner {
      height: 44px;
      line-height: 44px;
      background: #f4f4f4;
      font-size: 14px;
      color: #666666;
    }
    .el-button {
      width: 100px;
      height: 44px;
      color: #fff;
      // background-color: #4f81f4;
    }
    .el-form-item {
      border: none;
      border-radius: 4px;
      color: #666666;
    }
    .el-button--primary {
      color: #fff;
      background: #4f81f4;
      border-radius: 4px;
      border: none;
    }
    .check-wrap {
      display: block;
      width: 336px;
      margin: 0 auto 22px;
    }
    .el-checkbox__input.is-checked .el-checkbox__inner,
    .el-checkbox__input.is-indeterminate .el-checkbox__inner {
      background-color: #4f81f4;
      border-color: #4f81f4;
    }
    .el-checkbox__input.is-checked + .el-checkbox__label {
      color: #4f81f4;
    }
    .userProtocol {
      display: inline-block;
      font-size: 14px;
      margin-left: 5px;
      color: #d37015;
      cursor: pointer;
    }
    // ------弹出框 start ------
    .el-dialog {
      width: 670px;
      height: 788px;
      border-radius: 12px;
      margin-top: 8vh !important;
      box-shadow: transparent;
    }
    .el-dialog__header {
      padding: 0;
    }
    .el-dialog__title {
      font-size: 18px;
      color: #444444;
      text-align: center;
      padding: 25px 0;
      border-bottom: 1px solid #ebebeb;
      display: block;
    }
    .el-dialog__body {
      padding: 0;
      height: 675px;
      overflow-y: scroll;
      padding: 0 15px;
    }
    .el-dialog__headerbtn .el-dialog__close {
      font-size: 24px;
      vertical-align: -webkit-baseline-middle;
    }
    /* 滚动条 */
    ::-webkit-scrollbar-track-piece {
      background-color: #f8f8f8;
    }
    ::-webkit-scrollbar {
      width: 5px;
      height: 30px !important;
    }
    ::-webkit-scrollbar-thumb {
      height: 30px !important;
      background: #cacaca;
      border-radius: 100px;
      background-clip: padding-box;
    }
    .aboutRulesWrap {
      margin-bottom: 40px;
    }
    .tip {
      margin: 20px auto;
      font-size: 18px;
      color: #444;
    }
    .rulesTitle {
      font-size: 18px;
      color: #444444;
      margin-bottom: 18px;
    }
    .rulesList {
      padding-left: 20px;
    }
    .rulesList li {
      font-size: 14px;
      color: #2a2a2a;
      letter-spacing: 0.37px;
      line-height: 28px;
      padding-right: 20px;
      overflow-x: hidden;
    }
    .rulesList li span {
      font-size: 16px;
      color: #444444;
    }
    .rulesPaddingBttom {
      padding-bottom: 25px;
    }
    .rulesItemList {
      padding-top: 15px;
    }
    .rulesItemList > li {
      padding-left: 52px;
      font-size: 14px;
      color: #666666;
      line-height: 28px;
    }
    .rulesItemList > li::before {
      content: "";
      width: 8px;
      height: 8px;
      line-height: 28px;
      background-color: #d8d8d8;
      border-radius: 50%;
      display: inline-block;
      margin-right: 8px;
    }
    .rulesItemList > li.rulesPaddingRight0 {
      padding-right: 0;
    }
    .rulesItemChild {
      width: 100%;
      background: #f6f6f6;
      margin-top: 10px;
      padding: 20px 30px;
    }
    // ------弹出框 end ------
  }
}

// 下拉选择 start
.area__item {
  height: 40px;
  font-size: 14px;
  color: #282828;
}

.area.selected {
  color: #d37015;
}

.area.hover,
.area:hover {
  background: #f2f2f2;
}

// 下拉选择 end

/*=============================================
              (max-width: 1023px)
      =============================================*/

@media all and (max-width: 1023px) {
  .password-container {
    .register-form {
      .el-input__inner {
        height: 1.17rem;
        line-height: 1.17rem;
        font-size: 0.37rem;
      }
      .el-input {
        font-size: 0.37rem;
      }
      .el-button {
        width: 2.67rem;
        height: 1.17rem;
        font-size: 0.37rem;
      }
      .el-form-item {
        margin: 0 auto 0.59rem;
        width: 90%;
      }
      .el-form-item__content {
        line-height: 1.17rem;
        font-size: 0.37rem;
      }
      .el-select {
        width: 2.4rem;
        font-size: 0.37rem;
      }
      .el-form-item__error {
        font-size: 0.32rem;
      }
      .el-checkbox__inner {
        width: 0.37rem;
        height: 0.37rem;
      }
      .el-checkbox__label {
        padding-left: 0.27rem;
        line-height: 0.51rem;
        font-size: 0.37rem;
      }
      .el-checkbox__inner::after {
        height: 0.19rem;
        left: 0.11rem;
        width: 0.08rem;
      }
      .el-dialog {
        width: 100%;
        height: 15rem;
        border-radius: 0.32rem;
      }
      .el-dialog__title {
        font-size: 0.48rem;
        padding: 0.67rem 0;
        line-height: 0.64rem;
      }
      .el-dialog__body {
        height: 11.8rem;
        padding: 0 0.4rem;
      }
      .el-dialog__headerbtn .el-dialog__close {
        font-size: 0.64rem;
      }
    }
  }
  .el-select-dropdown__item {
    font-size: 0.37rem;
    padding: 0 0.53rem;
    height: 0.91rem;
    line-height: 0.91rem;
  }
  .el-select-dropdown__item span {
    line-height: 0.91rem !important;
  }
  .el-select .el-input .el-select__caret {
    font-size: 0.37rem;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg: #f4f4f4;
$dark_gray: #889aa4;
$light_gray: #eee;
.password-container {
  // position: fixed;
  height: 100%;
  width: 100%;
  background-color: $bg;
  .register-form {
    position: absolute;
    left: 0;
    right: 0;
    width: 900px;
    margin: 140px auto;
    padding-bottom: 50px;
    background-color: #fff;
    .username {
      width: 241px;
    }
    h3 {
      padding: 24px 0;
      font-size: 24px;
      border-bottom: 1px solid #dddddd;
      color: #444444;
    }
  }
  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
    &_login {
      font-size: 20px;
    }
  }
  .title {
    font-size: 26px;
    font-weight: 400;
    color: $light_gray;
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}

.login-nav {
  line-height: 76px;
  overflow: hidden;
  background: #f4f4f4;
}

.login-nav h2 {
  font-size: 28px;
  color: #282828;
  float: left;
}

.login-nav h2 span {
  font-size: 24px;
  color: #444444;
  margin-left: 20px;
}

.login-nav .nav {
  float: right;
  font-size: 14px;
  color: #444444;
}

.login-nav .nav .toLogin,
.login-nav .nav .return {
  cursor: pointer;
  color: #d37015;
}

.login-nav .nav .divider {
  display: inline-block;
  width: 1px;
  background: #666666;
  height: 14px;
  margin: 0 18px;
  vertical-align: middle;
}

.smcode {
  width: 120px;
}

.smcode-wrap {
  margin: 0 auto 22px;
  height: 44px;
  width: 336px;
  .el-form-item {
    display: inline-block;
    width: 120px;
    margin: 0;
    .el-button {
      width: 120px;
    }
  }
}

/*=============================================
            max-width: 1023px)
          =============================================*/

@media all and (max-width: 1023px) {
  .container,
  .wrap {
    width: 100%;
  }
  .password-container {
    position: relative;
    .login-nav {
      line-height: 2.03rem;
      h2 {
        font-size: 0.75rem;
        padding-left: 0.27rem;
        span {
          font-size: 0.64rem;
          margin-left: 0.53rem;
        }
      }
      .nav {
        font-size: 0.37rem;
        padding-right: 0.53rem;
      }
    }
    .title {
      font-size: 0.69rem;
      margin: 0px auto 1.07rem;
    }
    .register-form {
      width: 100%;
      margin: 1rem auto;
      padding-bottom: 1.33rem;
      h3 {
        padding: 0.64rem 0;
        font-size: 0.64rem;
      }
      .check-wrap {
        width: 90%;
        margin: 0 auto 0.59rem;
      }
      .username {
        width: 6.43rem;
      }
      .userProtocol {
        font-size: 0.37rem;
        margin-left: 0.13rem;
      }
    }
    .rulesTitle {
      font-size: 0.48rem;
      margin-bottom: 0.48rem;
    }
    .tip {
      margin: 0.53rem auto;
      font-size: 0.48rem;
    }
    .rulesList {
      padding-left: 0.53rem;
    }
    .rulesList li {
      font-size: 0.37rem;
      letter-spacing: 0.01rem;
      line-height: 0.75rem;
      padding-right: 0.53rem;
    }
    .rulesItemList > li {
      padding-left: 0.27rem;
      font-size: 0.37rem;
      line-height: 0.75rem;
    }
    .rulesList li span {
      font-size: 0.43rem;
    }
    .rulesItemChild {
      width: 100%;
      margin-top: 0.27rem;
      padding: 0.27rem;
    }
  }
  .smcode-wrap .el-form-item {
    width: 3.2rem;
  }
  .smcode-wrap {
    margin: 0 auto 0.59rem;
    height: 1.17rem;
    width: 90%;
  }
  .smcode-wrap .el-form-item .el-button {
    width: 3.2rem;
    clear: both;
    display: inline-block;
  }
}
</style>
