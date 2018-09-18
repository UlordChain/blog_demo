<template>
  <div class="login-container">
    <el-form class="login-form" autoComplete="on" :model="loginForm" :rules="loginRules" ref="loginForm" label-position="left">
      <h3 class="title">Ulord博客系统</h3>
      <el-form-item prop="username">
        <el-input name="username" type="text"  v-model="loginForm.username" autoComplete="on" maxlength="11" placeholder="用户名" />
      </el-form-item>
      <el-form-item prop="password">
        <el-input name="password" :type="pwdType" @keyup.enter.native="handleLogin" v-model="loginForm.password" autoComplete="on" placeholder="密码" maxlength="16"></el-input>
      </el-form-item>
      <el-form-item style="text-align: center">
        <el-button v-bind:type="btn ? 'primary': 'info'" class="disabled" style="width:100%;" :disabled="!btn" :loading="loading" @click.native.prevent="handleLogin">
          登录
        </el-button>
        <router-link to="/register">注册即送SUT</router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { isvalidUsername } from "@/utils/validate";

export default {
  name: "login",
  data() {
    const validateUsername = (rule, value, callback) => {
      // if (!isvalidUsername(value)) {
      //   callback(new Error("请输入正确的手机号"));
      // } else {
      //   callback();
      // }
      callback();
    };
    const validatePass = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入密码"));
      } else if (value.length < 8) {
        callback(new Error("密码不能小于8位"));
      } else {
        callback();
      }
    };
    return {
      result: null,
      loginForm: {
        username: "",
        password: ""
      },
      loginRules: {
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
        ]
      },
      loading: false,
      pwdType: "password"
      // btn: Boolean(this.loginForm.username && this.loginForm.password)
    };
  },
  computed: {
    btn: function() {
      return Boolean(this.loginForm.username && this.loginForm.password);
    }
  },
  methods: {
    checkNo(value) {
      if (value) {
        setTimeout(() => {
          this.loginForm.username = this.loginForm.username.replace(/\D/g, "");
        }, 100);
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.result = Web3Helper.login(
            this.loginForm.username,
            this.loginForm.password
          );
          console.log(this.result,'result')
          if (this.result.result == 0) {
            this.$message({
              message: this.result.msg,
              type: "error"
            });
          } else if (this.result.result == 1) {
            this.loading = false;
            this.$store.dispatch('Login',this.result.msg)
            this.$message({
              message: '登录成功',
              type: 'success'
            })
            this.$router.push('/');
          }
        } else {
          console.log("error submit!!");
          return false;
        }
      });

      // if(Web3Helper.login(this.loginForm.username, this.loginForm.password).result == 0) {
      //   this.$message({
      //     message: Web3Helper.login(this.loginForm.username, this.loginForm.password).msg
      //   })
      // } else {
      //   console.log(Web3Helper.login(this.loginForm.username, this.loginForm.password).result)
      // }

      // this.$router.push({
      //   path: "/"
      // });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss">
/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    input {
      background: transparent;
      -webkit-appearance: none;
      padding: 12px 5px 12px 15px;
      color: #000;
      &:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px #fff inset !important;
        -webkit-text-fill-color: #000 !important;
      }
    }
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.login-container {
  // position: fixed;
  height: 100%;
  width: 100%;
  .login-form {
    position: absolute;
    left: 0;
    right: 0;
    width: 400px;
    margin: 140px auto;
    padding-bottom: 50px;
    background-color: #fff;
    h3 {
      padding: 24px 0;
      font-size: 24px;
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
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    cursor: pointer;
    user-select: none;
  }
}
</style>
