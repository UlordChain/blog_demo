<template>
  <div class="getTask-container">
     <div class="header-wrap">
      <top-Header></top-Header>
      </div>
    <div class="container">
      <div class="topTitle-wrap">
        领取任务
        <router-link to="/" class="topTitle-back">返回全部任务</router-link>
      </div>
      <div class="progress-wrap">
        <div class="step-wrap">
             <i class="step1-img"></i>
             <span class="active">申请</span>
        </div>
        <p class="progress-bar">
          <span class="progress-percent"></span>
        </p>
        <div class="step-wrap">
             <i class="step2-img"></i>
             <span>评选</span>
        </div>
         <p class="progress-bar"></p>
        <div class="step-wrap">
             <i class="step3-img"></i>
             <span>开发</span>
        </div>
         <p class="progress-bar"></p>
        <div class="step-wrap">
             <i class="step4-img"></i>
             <span>结束</span>
        </div>
      </div>
      <div class="getTask-detail-wrap">
          <h4>详细信息</h4>
          <el-form ref="getTaskForm" :model="getTaskForm" :rules="getTaskFormRules" class="form-container" label-width="180px">
            <el-form-item label="Github项目地址">
              <el-input v-model="getTaskForm.githubAddress" :disabled="!isOpen" class="mainNode-input-medium" maxlength="255"></el-input>
              <span class="input-tip">闭源项目不用填Github地址</span>
            </el-form-item>
            <el-form-item prop="walletAddress" label="钱包地址">
              <el-input v-model="getTaskForm.walletAddress" class="mainNode-input-large" maxlength="40"></el-input>
            </el-form-item>
             <el-form-item prop="fileUrl" label="方案&原型&开发计划" required>
               {{getTaskForm.fileName}}
              <el-upload
                class="upload"
                ref="upload"
                action="https://upload.qiniup.com/"
                :data = "uploadData"
                :show-file-list="false"
                :auto-upload="false"   
                :on-success="handleAvatarSuccess"
                 :on-change="handleChangeUpload"
                :before-upload="beforeAvatarUpload"
                :on-progress="uploadFileProcess">
                <!-- <i  class="el-icon-plus avatar-uploader-icon"></i> -->
                <el-button type="primary" class="submit-btn">上传附件</el-button>
                <span class="input-tip">附近格式为zip，不大于30MB</span>
              </el-upload>
              <el-progress v-if="fileFlag == true" type="circle" :percentage="Number(fileUploadPercent.percentage.toFixed(0))"></el-progress>
            </el-form-item>
             <el-form-item label="额外申请材料链接" prop="materials">
              <el-input v-model="getTaskForm.materials" class="mainNode-input-large" maxlength="255"></el-input>
            </el-form-item>
             <el-form-item prop="emailAddress" label="邮箱">
              <el-input v-model="getTaskForm.emailAddress" class="mainNode-input-large" maxlength="255"></el-input>
            </el-form-item>
            <el-form-item  label="团队人员介绍" prop="devTeam">
              <!-- <el-input v-model="getTaskForm.devTeam" type="textarea" :rows="2" placeholder="请输入内容" class="mainNode-input-large"></el-input> -->
              <el-input
                type="textarea"
                :autosize="{ minRows: 2, maxRows: 4}"
                placeholder="请输入内容"
                v-model="getTaskForm.devTeam" class="mainNode-input-large"
                 maxlength="2000">
              </el-input>
            </el-form-item>
            <el-form-item class="submit-btn-wrap">
              <el-button @click.prevent="submit" v-bind:type="btn ? 'primary': 'info'"  class="submit-btn-large">申请</el-button>
            </el-form-item>
          </el-form>
      </div>

    </div>
  </div>
</template>
<script>
import { validateEmail, txId, validateURL } from "@/utils/validate";
import { getToken } from "@/utils/auth";
import { submitTask, getQiToken } from "@/api/api";
import { apiUrl } from "@/api/url";
export default {
  name: "taskApply",
  data() {
    const validateEmail2 = (rule, value, callback) => {
      if (!validateEmail(value)) {
        callback(new Error("请输入正确的邮箱"));
      } else {
        callback();
      }
    };
    const validateAddress = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入钱包地址"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的钱包地址"));
      } else if (value.length < 40 && value.length > 30) {
        callback();
      } else {
        callback(new Error("交易地址限制在30-40字符内"));
      }
    };
    const validateExtraUrl = (rule, value, callback) => {
      if (!value) {
        callback();
      } else if (!validateURL(value)) {
        callback(new Error("请填写正确的链接"));
      } else {
        callback();
      }
    };
    return {
      uploadData: {},
      isOpen: Boolean(this.$route.query.isOpenSource),
      fileFlag: false,
      getTaskForm: {
        githubAddress: "",
        walletAddress: "",
        materials: "",
        emailAddress: "",
        fileName: "",
        fileUrl: "",
        devTeam: ""
      },
      getTaskFormRules: {
        walletAddress: [
          { required: true, trigger: "blur", validator: validateAddress }
        ],
        emailAddress: [
          { required: true, trigger: "blur", validator: validateEmail2 }
        ],
        fileUrl: [
          { required: true, trigger: "change", message: "请上传相应的文件" }
        ],
        materials: [{ trigger: "blur", validator: validateExtraUrl }],
        devTeam: [
          { required: true, trigger: "blur", message: "请输入团队成员介绍" }
        ]
      }
    };
  },
  computed: {
    btn: function() {
      return Boolean(
        this.getTaskForm.walletAddress &&
          this.getTaskForm.fileUrl &&
          this.getTaskForm.emailAddress &&
          this.getTaskForm.devTeam
      );
    }
  },
  methods: {
    submit() {
      this.$refs.getTaskForm.validate(valid => {
        if (valid) {
          this.$confirm("是否继续提交？", "提示", {
            confirmButtonText: "提交",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            submitTask(
              this.getTaskForm.materials,
              this.$route.query.id,
              this.getTaskForm.emailAddress,
              this.getTaskForm.githubAddress,
              this.$route.query.isOpenSource,
              this.getTaskForm.fileUrl,
              this.getTaskForm.devTeam,
              this.getTaskForm.walletAddress
            ).then(res => {
              if (res.success) {
                this.$message({
                  type: "success",
                  message: "提交成功!"
                });
                this.$router.push("/personal/myTask");
              } else if (res.errorCode == "200001") {
                this.$message({
                  type: "error",
                  message: res.errorMsg
                });
              }
            });
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    //上传成功
    handleAvatarSuccess(res, file) {
      this.getTaskForm.fileName = file.name;
      this.getTaskForm.fileUrl = res.url + "?attname=" + file.name;
      this.$refs.getTaskForm.validateField("fileUrl", fileFlag => {});
    },

    //上传前
    beforeAvatarUpload(file) {
      // console.log(file.name.substr(file.name.length-3,3));
      const isLt5M = file.size / 1024 / 1024 < 30;
      const extension1 = file.name.substr(file.name.length - 3, 3) === "zip";
      if (!extension1) {
        this.$message.error("上传文件只能是 zip 格式!");
        return false;
      } else if (!isLt5M) {
        this.$message.error("上传文件大小不能超过 30MB!");
        return false;
      } else {
        return true;
      }
    },
    handleChangeUpload(file) {
      getQiToken(file.name).then(res => {
        if (res.success) {
          this.uploadData = {
            token: res.token
          };
          setTimeout(this.uploadAction, 500);
        } else {
          return false;
        }
      });
    },
    uploadAction() {
      this.$refs.upload.submit();
    },
    //上传中
    uploadFileProcess(event, file, fileList) {
      this.fileFlag = true;
      this.fileUploadPercent = file;
    }
  }
};
</script>
<style lang="scss">
.getTask-container {
  .upload {
    display: inline-block;
  }
  .el-progress {
    margin: 0 !important;
  }
  .el-progress-circle {
    margin: 0 !important;
    width: 46px !important;
    height: 46px !important;
  }
  .el-form-item__content * {
    vertical-align: middle;
  }
  .el-form-item__label {
    text-align: left;
  }
  .el-form-item.is-required .el-form-item__label:after {
    content: "*";
    color: #f56c6c;
    margin-right: 4px;
  }
  .el-form-item.is-required .el-form-item__label:before {
    content: "";
    margin-right: 0;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
body {
  background-color: #ffffff;
}
.getTask-container {
  padding-bottom: 125px;
  .container {
    width: 1200px;
    margin: 0 auto;
  }
  .topTitle-wrap {
    margin-top: 40px;
    position: relative;
    height: 120px;
    line-height: 120px;
    font-size: 24px;
    color: #444444;
    text-align: center;
    border-bottom: 1px solid #eeeeee;
    font-weight: bold;
    .topTitle-back {
      position: absolute;
      font-size: 14px;
      color: #d37015;
      right: 30px;
      top: 4px;
    }
  }
  .progress-wrap {
    width: 100%;
    height: 200px;
    padding-top: 59px;
    margin: 0 auto;
    text-align: center;
    .step-wrap {
      // margin-right: 126px;
      display: inline-block;
      &:last-child {
        margin-right: 0;
      }
      span {
        font-size: 14px;
        color: #a5a5a5;
        display: block;
        text-align: center;
      }
      span.active {
        font-size: 18px;
        color: #4f81f4;
      }
    }
  }
  .progress-bar {
    display: inline-block;
    width: 126px;
    height: 4px;
    background: #f1f1f1;
    margin-bottom: 62px;
  }
  .progress-percent {
    display: block;
    width: 70px;
    height: 4px;
    background: #4f81f4;
    margin-bottom: 62px;
  }
  .step1-img {
    display: inline-block;
    width: 94px;
    height: 100px;
    background: url(../assets/getTask-icon-01.png) no-repeat center bottom;
  }
  .step2-img {
    display: inline-block;
    width: 102px;
    height: 100px;
    background: url(../assets/getTask-icon-02.png) no-repeat center bottom;
  }
  .step3-img {
    display: inline-block;
    width: 94px;
    height: 100px;
    background: url(../assets/getTask-icon-03.png) no-repeat center bottom;
  }
  .step4-img {
    display: inline-block;
    width: 102px;
    height: 100px;
    background: url(../assets/getTask-icon-04.png) no-repeat center bottom;
  }
  .getTask-detail-wrap {
    clear: both;
    padding: 30px 0 20px;
    h4 {
      font-size: 18px;
      color: #444444;
      margin-bottom: 40px;
      padding-left: 90px;
    }
    // 输入框 start
    .el-form-item__label {
      width: 181px;
      text-align: left;
    }
    .form-container {
      padding-left: 110px;
    }
    .el-form-item {
      margin: 0 auto;
      margin-bottom: 20px;
      &:first-child {
        margin-top: 25px;
      }
    }
    .el-form-item__content {
      line-height: 44px;
    }
    .el-form-item__content > span {
      width: 181px;
      height: 44px;
      text-align: left;
      display: inline-block;
      font-size: 14px;
      color: #999999;
    }
    .el-form-item__content .input-tip {
      font-size: 14px;
      color: #a9a9b3;
      margin-left: 10px;
    }
    .el-input {
      height: 44px;
      width: 280px;
      display: inline-block;
    }
    .el-input__inner {
      height: 44px;
      background: #f4f4f4;
      border: 1px solid #dddddd;
      font-size: 14px;
      color: #666666;
    }
    .mainNode-input-medium {
      width: 500px;
      .el-input__inner {
        width: 100%;
        height: 44px;
        line-height: 44px;
        background: #f4f4f4;
        font-size: 14px;
        color: #666666;
      }
    }
    .mainNode-input-large {
      width: 797px;
      .el-input__inner {
        width: 100%;
        height: 44px;
        line-height: 44px;
        background: #f4f4f4;
        font-size: 14px;
        color: #666666;
      }
    }
    .star {
      &::after {
        content: "*";
        display: inline-block;
        color: red;
        vertical-align: top;
      }
    }

    // 输入框 end
    // error tip
    .el-form-item__error {
      left: 17%;
    }
    // 文本域 start
    .el-textarea {
      width: 797px;
      display: inline-block;
    }
    .el-textarea__inner {
      min-height: 44px !important;
      padding: 10px 15px 0;
      font-size: 14px;
      color: #666666;
      background: #f4f4f4;
      border: 1px solid #dddddd;
      border-radius: 4px;
    }
    // 文本域 end
  }
  // 提交按钮 start
  .submit-btn-wrap {
    margin: 0 auto;
    text-align: center;
  }
  .submit-btn {
    background: #4f81f4;
    width: 100px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
  }
  .el-button--primary:focus,
  .el-button--primary:hover {
    background: #4f81f4;
    width: 100px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
  }
  .submit-btn-large {
    width: 320px;
    height: 60px;
    line-height: 60px;
    padding: 0;
    font-size: 18px;
    color: #ffffff;
    margin-top: 80px;
  }
  .submit-btn-large.el-button--primary:focus,
  .submit-btn-large.el-button--primary:hover {
    background: #4f81f4;
    width: 320px;
    height: 60px;
    line-height: 60px;
    padding: 0;
    font-size: 18px;
    color: #ffffff;
  }
  // 提交按钮 end
  .team-detail-wrap {
    padding: 30px 0 20px;
    border-bottom: 1px solid #eeeeee;
    h4 {
      font-size: 18px;
      color: #444444;
      margin-bottom: 40px;
      padding-left: 90px;
    }
  }
}
</style>

