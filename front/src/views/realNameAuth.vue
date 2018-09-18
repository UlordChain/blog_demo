<template>
<div v-if="!loading" class="realNameAuth-container">
  <div class="topTitle-wrap">
    实名认证
    <router-link to="/personal/personalSetting" class="topTitle-back">返回个人设置</router-link>
  </div>
  <div class="form-container">
      <el-form v-if="status == 3"  name="realAuth" :model="authForm" :rules="realAuthFormRules" ref="realAuthForm" class="realAuthForm-wrap">
        <el-form-item class="borderNone">
          <span>国籍</span>
          <el-select v-model="authForm.value" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.index"
                :value="item"
               >
              </el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="name" class="aaa">
           <span>姓名</span>
           <el-input name="name" class="name" type="text" v-model="authForm.name" maxlength="30" autoComplete="off" placeholder="填写真实姓名" />
        </el-form-item>
        <el-form-item prop="email" class="aaa">
           <span>邮箱</span>
           <el-input name="email" class="email" type="text" v-model="authForm.email" maxlength="320" autoComplete="off" placeholder="填写邮箱" />
        </el-form-item>
        <el-form-item class="borderNone">
          <span>证件类型</span>
          <el-select v-model="authForm.value2" placeholder="请选择">
              <el-option
                v-for="item in options2"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                >
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item prop="idNumber" v-if="authForm.value2 == 0">
            <span>证件号码</span>
            <el-input name="idNumber" class="idNumber" type="text" v-model="authForm.idNumber" maxlength="18" autoComplete="off" placeholder="填写证件号码" />
        </el-form-item>
         <el-form-item prop="idNumber" v-if="authForm.value2 == 1">
            <span>证件号码</span>
            <el-input name="idNumber" class="idNumber" type="text" v-model="authForm.idNumber" maxlength="18" autoComplete="off" placeholder="填写证件号码" />
        </el-form-item>
        <el-form-item  prop="imageUrl1" class="idCard-wrap height120">
          <span class="alignTop">身份认证</span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess1"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl1" :src="authForm.imageUrl1" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">添加身份证或护照正面照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item prop="imageUrl2" class="idCard-wrap height120">
          <span></span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess2"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl2" :src="authForm.imageUrl2" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">添加身份证或护照反面照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item prop="imageUrl3" class="idCard-wrap height120">
          <span></span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess3"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl3" :src="authForm.imageUrl3" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">手持身份证或护照上半身照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item class="uploader-tip-wrap">
          <span></span>
          <p class="uploader-tip">上传照片不超过2MB，仅限PNG、JPG格式</p>
        </el-form-item>
        <el-form-item>
          <span></span>
          <el-button type="primary" @click.prevent.native="submit" class="ran-submit-btn">保存</el-button>
        </el-form-item>
      </el-form>
      <div v-if="status == 0" class="submited-wrap">
        <div class="submited-title">
          <i class="el-icon-circle-check submited-icon"></i>
          <span>申请已提交</span>
        </div>
        <div class="submited-content">已经收到您的申请，我们会尽快审核并向您反馈结果。</div>
      </div>
      <div v-if="status == 1" class="passed-wrap">
        <div class="passed-title">
          <i class="el-icon-circle-check passed-icon"></i>
          <span>申请已通过</span>
        </div>
        <div class="ran-info-wrap">
          <span>国籍: </span>
          <div>{{value}}</div>
        </div>
        <div class="ran-info-wrap">
          <span>姓名: </span>
          <div>{{name}}</div>
        </div>
        <div class="ran-info-wrap">
          <span>证件号: </span>
          <div>{{idNumber}}</div>
        </div>
        <div class="ran-info-wrap">
          <span>手机号: </span>
          <div>{{phone}}</div>
        </div>
      </div>
      <div v-if="status == 2" class="refused-wrap">
        <div class="refused-title">
          <i class="el-icon-remove refused-icon"></i>
          <span>申请未通过</span>
        </div>
        <div class="refused-content">抱歉，由于您的{{refuseInfo}}，未能通过审核。</div>
        <div class="reapply-content">
          您可以
          <span @click="again">重新申请</span>
        </div>
      </div>
      <el-form v-if="status == 4"  name="realAuth" :model="authForm" :rules="realAuthFormRules" ref="realAuthForm" class="realAuthForm-wrap">
        <el-form-item class="borderNone">
          <span>国籍</span>
          <el-select v-model="authForm.value" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.index"
                :value="item"
               >
              </el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="name" class="aaa">
           <span>姓名</span>
           <el-input name="name" class="name" type="text" v-model="authForm.name" maxlength="30" autoComplete="off" placeholder="填写真实姓名" />
        </el-form-item>
        <el-form-item prop="email" class="aaa">
           <span>邮箱</span>
           <el-input name="email" class="email" type="text" v-model="authForm.email" maxlength="320" autoComplete="off" placeholder="填写邮箱" />
        </el-form-item>
        <el-form-item class="borderNone">
          <span>证件类型</span>
          <el-select v-model="authForm.value2" placeholder="请选择">
              <el-option
                v-for="item in options2"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                >
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item prop="idNumber" v-if="authForm.value2 == 0">
            <span>证件号码</span>
            <el-input name="idNumber" class="idNumber" type="text" v-model="authForm.idNumber" maxlength="18" autoComplete="off" placeholder="填写证件号码" />
        </el-form-item>
         <el-form-item prop="idNumber" v-if="authForm.value2 == 1">
            <span>证件号码</span>
            <el-input name="idNumber" class="idNumber" type="text" v-model="authForm.idNumber" maxlength="18" autoComplete="off" placeholder="填写证件号码" />
        </el-form-item>
        <el-form-item  prop="imageUrl1" class="idCard-wrap height120">
          <span class="alignTop">身份认证</span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess1"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl1" :src="authForm.imageUrl1" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">添加身份证或护照正面照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item prop="imageUrl2" class="idCard-wrap height120">
          <span></span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess2"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl2" :src="authForm.imageUrl2" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">添加身份证或护照反面照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item prop="imageUrl3" class="idCard-wrap height120">
          <span></span>
          <el-upload
            class="avatar-uploader"
            :action="url"
            :data = "aaa"
            :headers = "headerData"
            :show-file-list="false"
            :on-success="handleAvatarSuccess3"
            :before-upload="beforeAvatarUpload">
            <img v-if="authForm.imageUrl3" :src="authForm.imageUrl3" class="avatar">
            <i v-else class="el-icon-circle-plus-outline avatar-uploader-icon"></i>
            <p class="uploader-explain">手持身份证或护照上半身照片</p>
          </el-upload>
        </el-form-item>
        <el-form-item class="uploader-tip-wrap">
          <span></span>
          <p class="uploader-tip">上传照片不超过2MB，仅限PNG、JPG格式</p>
        </el-form-item>
        <el-form-item>
          <span></span>
          <el-button type="primary" @click.prevent.native="submitPut" class="ran-submit-btn">保存</el-button>
        </el-form-item>
      </el-form>
  </div>

  <!-- <button @click="yyy">123</button> -->
</div>

</template>
<script>
import { getToken } from "@/utils/auth";
import countrys from "@/components/countrys";
import { realNameAuth, getAuthStatus,realNameAuthPut } from "@/api/api";
import { validateEmail, validateMainName2, isvalidUsername, validateNickName } from "@/utils/validate";
import { apiUrl } from "@/api/url";
import store from '../store'
export default {
  data() {
    const validateName = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入正确的姓名"));
      }
      if (value.length > 30) {
        callback(new Error("姓名最长不超过30个字符"));
      } else {
        callback();
      }
    };
    const validateEmailRight = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入邮箱"));
      }
      if (!validateEmail(value)) {
        callback(new Error("请输入正确的邮箱"));
      } else {
        callback();
      }
    };
    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入证件号"));
      }
      if (!validateMainName2(value)) {
        callback(new Error("请输入正确的证件号"));
      } else {
        callback();
      }
    };
    return {
      url: apiUrl + "/api/fileOperations/uploadFile.Action",
      loading: true,
      status: "",
      value: "",
      name: "",
      idNumber: "",
      phone: store.getters.name,
      email: "",
      refuseInfo: "",
      aaa: {
        directory: "identityCard"
      },
      headerData: {
        client_name: "jwt",
        token: getToken()
      },
      authForm: {
        name: "",
        imageUrl1: "",
        imageUrl2: "",
        imageUrl3: "",
        idNumber: "",
        value: "中国",
        value2: 0
      },
      imageUrl1: "",
      imageUrl2: "",
      imageUrl3: "",
      options: countrys,
      options2: [
        {
          value: 0,
          label: "身份证"
        },
        {
          value: 1,
          label: "护照"
        }
      ],
      realAuthFormRules: {
        name: [{ required: true, trigger: "blur", validator: validateName }],
        email: [
          { required: true, trigger: "blur", validator: validateEmailRight }
        ],
        idNumber: [
          { required: true, trigger: "blur", validator: validateIdCard }
        ],
        imageUrl1: [
          { required: true, message: "请上传对应的图片", trigger: "change" }
        ],
        imageUrl2: [
          { required: true, message: "请上传对应的图片", trigger: "change" }
        ],
        imageUrl3: [
          { required: true, message: "请上传对应的图片", trigger: "change" }
        ]
      },
      labelPosition: "left"
    };
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  },
  methods: {
    again() {
      this.status = 4;
    },
    handleAvatarSuccess1(res, file) {
      console.log(res.uri);
      this.imageUrl1 = res.uri;
      this.authForm.imageUrl1 = URL.createObjectURL(file.raw);
    },
    handleAvatarSuccess2(res, file) {
      console.log(res);
      this.imageUrl2 = res.uri;
      this.authForm.imageUrl2 = URL.createObjectURL(file.raw);
    },
    handleAvatarSuccess3(res, file) {
      console.log(res);
      this.imageUrl3 = res.uri;
      this.authForm.imageUrl3 = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      console.log(file);
      const isJPG = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;
     
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
       if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG和PNG 格式!");
      }
      return isLt2M && isJPG;
    },
    submit() {
      this.$refs.realAuthForm.validate(valid => {
        if (valid) {
          this.$confirm("实名认证资料提交后不能修改,是否继续提交？", "提示", {
            confirmButtonText: "提交",
            cancelButtonText: "取消",
            type: "warning",
            customClass: "rna-popWrap"
          }).then(() => {
            realNameAuth(
              this.authForm.name,
              this.authForm.email,
              this.authForm.value,
              this.authForm.value2,
              this.authForm.idNumber,
              this.imageUrl1,
              this.imageUrl2,
              this.imageUrl3
            ).then((res) => {
              // console.log('123',res.errorCode);
              if (res.success) {
                this.$message({
                  type: "success",
                  message: "提交成功!"
                });
                location.reload();
              } else if (res.errorCode == "200001"){
                this.$message({
                  type: 'error',
                  message: '身份证号码验证错误'
                })
              }
            });
          });
          // .catch(() => {
          //   this.$message({
          //     type: "info",
          //     message: "已取消删除"
          //   });
          // });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
      },
      submitPut() {
         this.$refs.realAuthForm.validate(valid => {
        if (valid) {
          this.$confirm("实名认证资料提交后不能修改,是否继续提交？", "提示", {
            confirmButtonText: "提交",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            realNameAuthPut(
              this.authForm.name,
              this.authForm.email,
              this.authForm.value,
              this.authForm.value2,
              this.authForm.idNumber,
              this.imageUrl1,
              this.imageUrl2,
              this.imageUrl3
            ).then(res => {
              if (res.success) {
                this.$message({
                  type: "success",
                  message: "提交成功!"
                })
                location.reload();
              } else if (res.errorCode == "200001") {
                this.$message({
                  type: 'error',
                  message: '身份证号码验证错误'
                })
              }
            });
          });
          // .catch(() => {
          //   this.$message({
          //     type: "info",
          //     message: "已取消删除"
          //   });
          // });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    getInfo() {
      console.log('22')
      this.loading = true;
      getAuthStatus()
        .then(res => {
          console.log(res);
          if (res.errorCode == "100003") {
            this.status = 3;
            this.loading = false;
          } else {
            if (res.identityDo.auditStatus == 0) {
              this.status = 0;
              this.loading = false;
            } else if (res.identityDo.auditStatus == 1) {
              this.status = 1;
              this.value = res.identityDo.nationality;
              this.name = res.identityDo.name;
              this.idNumber = res.identityDo.certificateNo;
              this.loading = false;
            } else if (res.identityDo.auditStatus == 2) {
              this.status = 2;
              this.refuseInfo = res.identityDo.remark;
              this.loading = false;
            }
          }
        })
        .catch(error => {
          this.loading = false;
        });
    }
    // yyy() {
    //   console.log('23');
    //   console.log(this.status);
    //   this.status = 3
    //   console.log(this.status);
    // }
  },
  mounted() {
    this.getInfo();
  }
};
</script>
<style rel="stylesheet/scss" lang="scss">
.realNameAuth-container{
  .form-container {
    .realAuthForm-wrap{
      .submited-title {
        margin-top: 37px;
        font-size: 16px;
        color: #666666;
        letter-spacing: 0.43px;
        text-align: center;
        vertical-align: middle;
        img {
          vertical-align: middle;
        }
      }
      .submited-content {
        margin-top: 28px;
        font-size: 16px;
        color: #666666;
        letter-spacing: 0.43px;
        text-align: center;
      }
      .avatar-uploader .el-upload {
        cursor: pointer;
        position: relative;
        overflow: hidden;
      }
      .avatar-uploader .el-upload:hover {
        border-color: #409eff;
      }
      .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 278px;
        height: 95px;
        text-align: center;
        background: #f4f4f4;
        border: 1px solid #dddddd;
        border-radius: 4px;
        padding-top: 23px;
      }
      .avatar {
        width: 278px;
        height: 120px;
        display: block;
        position: relative;
        z-index: 20;
      }

      .el-form-item {
        margin: 0 auto;
        margin-bottom: 18px;
        width: 375px;
        &:first-child {
          margin-top: 24px;
        }
        .el-form-item__content > span {
          width: 90px;
          height: 44px;
          text-align: left;
          display: inline-block;
          font-size: 14px;
          color: #999999;
        }
        .avatar-uploader {
          height: 120px;
          display: inline-block;
        }
      }
      .el-select,
      .el-input {
        height: 44px;
        width: 280px;
        display: inline-block;
      }
      .el-form-item__content {
        line-height: 44px;
      }
      .el-input__inner {
        height: 44px;
        background: #f4f4f4;
        font-size: 14px;
        color: #666666;
      }
      .el-form-item__error {
        left: 95px;
      }
      .alignTop {
        vertical-align: top;
      }
      .borderNone .el-input__inner {
        border: none;
      }
      .el-icon-circle-plus-outline:before {
        content: "\E602";
        color: #4f81f4;
        font-size: 40px;
      }
      .uploader-explain {
        position: absolute;
        top: 70%;
        left: 20%;
        font-size: 14px;
        color: #666666;
        line-height: 20px;
        user-select: none;
        z-index: 2;
      }
      .idCard-wrap {
        height: 120px;
        margin-bottom: 21px;
        &:last-child {
          margin-bottom: 0;
        }
      }
      .uploader-tip-wrap {
        margin-bottom: 51px;
        .el-form-item__content > span {
          height: 0;
        }
        .el-form-item__content {
          line-height: normal;
        }
      }
      .uploader-tip {
        display: inline-block;
        font-size: 14px;
        color: #999999;
      }
      .ran-submit-btn {
        background: #4f81f4;
        border-radius: 4px;
        width: 120px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        margin-bottom: 67px;
        font-size: 14px;
        color: #ffffff;
      }
      .el-icon-arrow-up:before {
        content: "\E60C";
        color: #999999;
      }
      .el-button--primary:focus,
      .el-button--primary:hover {
        background: #4f81f4;
        border-radius: 4px;
        width: 120px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        margin-bottom: 67px;
        font-size: 14px;
        color: #ffffff;
      }
      .height120 .el-form-item__content {
        height: 120px;
      }
    }
  }

}
   // 选择下拉框 start
  .el-popper .popper__arrow {
    display: none;
  }
  .el-popper[x-placement^="bottom"] {
    margin-top: 0;
  }
  .el-select-dropdown {
    border: none;
    box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.5);
  }
  .el-select-dropdown__list {
    padding: 0;
  }
  .el-select-dropdown__item {
    font-size: 14px;
    color: #282828;
    height: 44px;
    line-height: 44px;
  }
  .el-select-dropdown__item.selected {
    font-size: 14px;
    color: #d37015;
    font-weight: normal;
  }
  .el-select-dropdown__item.hover,
  .el-select-dropdown__item:hover {
    background: #f2f2f2;
    font-size: 14px;
    color: #282828;
  }
  .el-select-dropdown__item span{
    padding: 0 15px;
  }
  // 选择下拉框 end
   // 弹框 start
  .el-message-box.rna-popWrap {
    width: 400px;
    height: 248px;
    padding: 0;
  }
  .rna-popWrap{
    .el-message-box__header {
      padding: 19px 0 29px;
    }
    .el-message-box__title {
      font-size: 24px;
      color: #444444;
      text-align: center;
    }
    .el-message-box__content {
      padding: 0;
    }
    .el-message-box__message {
      margin-bottom: 56px;
    }
    .el-message-box__message p {
      font-size: 16px;
      color: #444444;
      text-align: center;
      line-height: 28px;
      width: 214px;
      margin: 0 auto;
    }
    .el-icon-warning:before {
      content: "";
    }
    .el-message-box__btns {
      padding: 0;
      text-align: center;
      border-top: 1px solid #eeeeee;
    }
    .el-button--small {
      font-size: 18px;
      color: #999999;
      background: #fff;
      text-align: center;
      border: none;
      line-height: 64px;
      border-right: 1px solid #eeeeee;
      width: 50%;
      padding: 0;
      &:last-child {
        border: none;
      }
    }
    .el-message-box__btns button:nth-child(2) {
      margin-left: 0;
    }
    .el-button:focus,
    .el-button:hover {
      font-size: 18px;
      color: #444444;
      border-color: transparent;
      background-color: #ffffff;
    }
    .el-button--primary:focus,
    .el-button--primary:hover {
      font-size: 18px;
      color: #4f81f4;
    }
  }
  // 弹框 end


</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.realNameAuth-container{
  .topTitle-wrap {
    position: relative;
    padding: 20px 0;
    font-size: 18px;
    color: #444444;
    text-align: center;
    border-bottom: 1px solid #eee;
    .topTitle-back {
      position: absolute;
      font-size: 14px;
      color: #d37015;
      right: 30px;
      top: 20px;
    }
  }
  // 申请已提交
  .submited-wrap{
    padding-bottom: 263px;
    .submited-title{
      margin: 0 auto;
      padding-top: 110px;
      text-align: center;
      .submited-icon{
        font-size: 24px;
        color: #6BC00C;
      }
      span {
        font-size: 20px;
        color: #444444;
        vertical-align: bottom;
      }
    }
    .submited-content{
      font-size: 16px;
      color: #666666;
      text-align: center;
      margin-top: 28px;
    }
  }
  // 申请未通过
  .refused-wrap{
    padding-bottom: 263px;
    .refused-title{
      margin: 0 auto;
      padding-top: 110px;
      text-align: center;
      .refused-icon{
        font-size: 24px;
        color: #D37015;
      }
      span {
        font-size: 20px;
        color: #444444;
        vertical-align: bottom;
      }
    }
    .refused-content{
      font-size: 16px;
      color: #666666;
      text-align: center;
      margin-top: 28px;
    }
    .reapply-content{
      font-size: 14px;
      color: #A9A9B3;
      text-align: center;
      margin-top:20px;
      span{
        cursor: pointer;
        font-size: 14px;
        color: #000000;
        text-align: center;
      }
    }
  }
  // 申请已通过
  .passed-wrap{
    margin: 0 auto;
    text-align:center;
    padding-bottom: 263px;
    .passed-title{
      margin: 0 auto;
      padding-top: 33px;
      text-align: center;
      margin-bottom: 42px;
      .passed-icon{
        font-size: 24px;
        color: #4F81F4;
      }
      span {
        font-size: 20px;
        color: #444444;
        vertical-align: bottom;
      }
    }
    .ran-info-wrap{
      margin-bottom:20px;
      span{
        width: 65px;
        font-size: 14px;
        color: #999999;
        display: inline-block;
        text-align: left;
      }
      div{
        display: inline-block;
        background: #F4F4F4;
        border-radius: 4px;
        width: 244px;
        height: 44px;
        line-height: 44px;
        padding: 0 18px;
        text-align: left;
        font-size: 14px;
        color: #666666;
      }
    }
  }
}
</style>
