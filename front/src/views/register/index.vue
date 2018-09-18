<template>
  <div class="register-container">
    <el-form class="register-form" autoComplete="on" :model="registerForm" :rules="registerRules" ref="registerForm" label-position="left">
      <h3 class="title">注册</h3>
      <el-form-item prop="nickName">
        <el-input name="nickName" class="nickName" type="text" maxlength="20" v-model="registerForm.nickName" autoComplete="on" placeholder="用户名" />
      </el-form-item>
      
      <el-form-item prop="password">
        <el-input name="password" type="password" @keyup.enter.native="handleLogin" v-model="registerForm.password" autoComplete="on" maxlength="16" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input name="password" type="password"  v-model="registerForm.confirmPassword" autoComplete="on" maxlength="16" placeholder="请再次确认密码"></el-input><i v-if="isPassWord" class="password-icon"></i>
      </el-form-item>
      
      <!-- <el-form-item prop="username">
        <el-input name="username" class="username" type="text" @input="checkNo(registerForm.username)"  v-model="registerForm.username" autoComplete="on" maxlength="11" placeholder="手机号" />
      </el-form-item>
      <el-form-item prop="email">
        <el-input name="email" class="email" type="text" @input="checkNo(registerForm.email)"  v-model="registerForm.email" autoComplete="on" maxlength="30" placeholder="邮箱" />
      </el-form-item> -->
      <el-form-item style="text-align: center">
        <el-button v-bind:type="btn ? 'primary': 'info'" :disabled="!btn" style="width:100%;" :loading="loading" @click.native.prevent="handleRegister">
          注册
        </el-button>
        <span>
          已有账号 <router-link to="/login">登录</router-link>
        </span>
        
      </el-form-item>
        
      
    </el-form>
  </div>
</template>

<script>
import { getsmscode, verifyPhone, verifyUsername, smVerify } from "@/api/api";
import { isvalidUsername, userName } from "@/utils/validate";
export default {
  name: "register",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!isvalidUsername(value)) {
        callback(new Error("请输入正确的手机号"));
      } else if (isvalidUsername(value)) {
        verifyPhone(value, parseInt(this.registerForm.value)).then(res => {
          if (res.data.success) {
            callback(new Error("该手机号已被注册"));
          } else {
            callback();
          }
        });
      } else {
        callback();
      }
    };
    const validateName = (rule, value, callback) => {
      if (!value) {
        callback(new Error("昵称不能为空"));
      } else if (!userName(value)) {
        callback(new Error("请输入正确的昵称"));
      } 
      // else if (value && userName(value)) {
      //   verifyUsername(value).then(res => {
      //     if (res.data.errorCode == "3000") {
      //       callback(new Error(res.data.errorMsg));
      //     } else if (res.data.errorCode == "1013") {
      //       callback(new Error(res.data.errorMsg));
      //     } else {
           
      //       callback();
      //     }
      //   });
      // }
       else {
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
        callback(new Error("密码不能小于8位"));
      } else if (value.length > 16) {
        callback(new Error("密码不能大于16位"));
      } else {
        callback();
        this.$refs.registerForm.validateField('confirmPassword')
      }
    };
    return {
      result: "",
      isPassWord: false,
      registerForm: {
        username: "",
        password: "",
        smcode: "",
        confirmPassword: "",
        nickName: "",
        checked: false,
        value: "+86"
        // valueT: parseInt(String(this.registerForm.value).replace('+',''))
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
        ],
        nickName: [
          {
            required: true,
            trigger: "blur",
            validator: validateName
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
        // this.registerForm.username &&
          this.registerForm.password &&
          // this.registerForm.smcode &&
          this.registerForm.nickName &&
          // this.registerForm.checked && 
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
          this.result =  Web3Helper.register(this.registerForm.nickName, this.registerForm.password);
          if(this.result.result == 0) {
            this.loading = false;
            this.$message({
              message: this.result.msg,
              type: 'error'
            })
          } else if (this.result.result == 1) {
            this.loading = false;
            this.$store.dispatch('Register',this.result.msg)
            this.$message({
              message: '注册成功',
              type: 'success'
            })
            this.$router.push('/');
          }
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

/* reset element-ui css */
.register-container {
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
$bg: #f4f4f4;
$dark_gray: #889aa4;
$light_gray: #eee;
.register-container {
  .password-icon {
    position: absolute;
    bottom: 12px;
    display: inline-block;
    width: 20px;
    height: 20px;
  }
  // position: fixed;
  height: 100%;
  width: 100%;
  background-color: $bg;
  .register-form {
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

</style>
