<template>
  <div class="newPwdContainer">
    <div class="title">修改密码
      <div class="return" @click="goP">返回个人设置</div>
    </div>
    <el-form :model="newPassForm" :rules="newPassRules" ref="newPassForm" class="newPwdForm-wrap">
      <el-form-item prop="currentPassword">
        <span>当前密码</span>
        <el-input name="currentPassword" class="currentPassword" type="password"  v-model="newPassForm.currentPassword" autoComplete="off" placeholder="" />
      </el-form-item>
      <el-form-item prop="newPassword">
        <span>新密码</span>
        <el-input name="newPassword" class="newPassword" type="password"  v-model="newPassForm.newPassword" autoComplete="off" placeholder="" />
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <span>确认新密码</span>
        <el-input name="confirmPassword" class="confirmPassword" type="password"  v-model="newPassForm.confirmPassword" autoComplete="off" placeholder="" />
      </el-form-item>
      <el-form-item>
        <span></span>
        <el-button v-bind:type="btn ? 'primary': 'info'" style="width:100%;" :loading="loading" @click.native.prevent="save" class="npd-save-btn" :disabled="!btn">
          保存
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { resetPassword } from "@/api/api"
import { getId } from "@/utils/auth"
export default {

  data() {
    const validateNewPassword = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error("密码不能小于8位"));
      } else if (value.length > 16) {
        callback(new Error("密码不能大于16位"))
      } else {
        callback();
      }
    };
    const validateConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入正确的密码"));
      } else if (value !== this.newPassForm.newPassword) {
        callback(new Error("密码不一致"));
      } else {
        callback();
      }
    };
    return {
      newPassForm: {
        currentPassword: "",
        newPassword: "",
        confirmPassword: ""
      },
      newPassRules: {
        currentPassword: [{ required: true, trigger: "blur", message: "请输入正确的密码" }],
        newPassword: [{ required: true, trigger: "blur", validator: validateNewPassword }],
        confirmPassword: [{ required: true, trigger: "blur", validator: validateConfirmPassword }]
      },
      loading: false
    }
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  },
  computed: {
    btn: function() {
      return Boolean(this.newPassForm.currentPassword && this.newPassForm.newPassword && this.newPassForm.confirmPassword)
    }
  },
  methods: {
    goP(){
      this.$router.push({path: '/personal/personalSetting'})
    },
    save() {
       this.$refs.newPassForm.validate(valid => {
        if (valid) {
          this.loading = true;
          resetPassword(this.newPassForm.currentPassword, this.newPassForm.newPassword, getId()).then(res => {
            console.log(res.data.errorCode) ;
            if(res.data.errorCode == 'OK') {
              this.loading = false;
              this.$message({
                message: '修改成功',
                type: 'success'
              })
              this.$router.push({path: '/personal/personalSetting'})
            }else if(res.data.errorCode == "1008"){
              this.$message({
                message: '当前密码错误！',
                type: 'error',
                duration: 5 * 1000
              })
              this.loading = false;
            }else if(res.data.errorCode == "1009"){
              this.$message({
                message: '密码输入错误次数太多，请明天再试！',
                type: 'error',
                duration: 5 * 1000
              })
              this.loading = false;
            }
          }).catch(() => {
              this.loading = false;
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    }
  }
}
</script>
<style rel="stylesheet/scss" lang="scss">
  .newPwdContainer{
    .newPwdForm-wrap{
      // 输入框 start
      .el-form-item {
          margin: 0 auto;
          margin-bottom: 20px;
          &:first-child {
            margin-top: 25px;
          }
      }
      .el-form-item__content{
        line-height: 44px;
      }
      .el-form-item__content>span{
        width: 181px;
        height: 44px;
        text-align: left;
        display: inline-block;
        font-size: 14px;
        color: #999999;
      }
      .el-input{
        height: 44px;
        width: 280px;
        display: inline-block;
      }
      .el-input__inner{
        height: 44px;
        background: #F4F4F4;
        border: 1px solid #DDDDDD;
        font-size: 14px;
        color: #666666;
      }
      .mainNode-input-medium{
        width: 500px;
        .el-input__inner{
          width: 100%;
          height: 44px;
          line-height: 44px;
          background: #F4F4F4;
          font-size: 14px;
          color: #666666;
        }
      }
      .mainNode-input-large{
        width: 797px;
        .el-input__inner{
          width: 100%;
          height: 44px;
          line-height: 44px;
          background: #F4F4F4;
          font-size: 14px;
          color: #666666;
        }
      }
      .star{
        &::after{
          content: '*';
          display: inline-block;
          color: red;
          vertical-align: top;
        }
      }
     // 输入框 end
    .el-button--primary {
        color: #fff;
        background-color: #4F81F4;
        border-color: #4F81F4;
    }
    }
  }
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.newPwdContainer .selectorBox .selectorList{
    width:282px;
}
.newPwdContainer .title,.asset-container .title {
    position: relative;
    height: 75px;
    line-height: 75px;
    font-size: 18px;
    color: #444444;
    text-align: center;
    font-weight: normal;
    border-bottom: 1px solid #eee;
}
.newPwdContainer .return,.asset-container .return {
    position: absolute;
    font-size: 14px;
    color: #D37015;
    right: 34px;
    top: 4px;
    font-weight: normal;
    cursor: pointer;
}

.newPwdContainer .information-box {
    margin-top: 25px;
}
.newPwdContainer{
  .el-form-item {
    margin: 0 auto;
    margin-bottom: 20px;
    width: 375px;
    &:first-child {
      margin-top: 25px;
    }
 }
  .el-form-item__content{
    line-height: 44px;
  }
  .el-form-item__content>span{
    width: 90px;
    height: 44px;
    text-align: left;
    display: inline-block;
    font-size: 14px;
    color: #999999;
  }
  .el-input{
    height: 44px;
    width: 280px;
    display: inline-block;
  }
  .el-input__inner{
    height: 44px;
    background: #F4F4F4;
    border: 1px solid #DDDDDD;
  }
  .el-form-item__error {
    left: 25%;
 }
 .npd-save-btn {
    display: inline-block;
    width: 120px!important;
    height: 44px;
    line-height: 44px;
    padding: 0;
    margin-bottom: 67px;
    font-size: 14px;
 }
}
</style>

