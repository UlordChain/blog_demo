<template>
  <div class="proposalForm-container">
    <div class="header-wrap">
      <top-Header></top-Header>
    </div>
    <div class="container">
         <div class="topTitle-wrap">
            提案申请表
            <!-- <router-link to="/personal/proposal" class="topTitle-back">返回提案管理</router-link> -->
         </div>
         <div class="proposalForm-content-wrap">
           <h4>提案基本信息</h4>
           <div class="proposalForm-box" >
              <el-form ref="proposalForm" :model="proposalForm" :rules="proposalFormRules" label-width="200px">
                <el-form-item prop="name" label="提案名" label-width="200px" label-position="right">
                  <el-input v-model="proposalForm.name" placeholder="填写唯一提案名" maxlength="30"></el-input>
                </el-form-item>
                <el-form-item  prop="ut" label="提案需求UT数" label-width="200px">
                  <el-input v-model="proposalForm.ut" type="text" maxlength="6" @input="checkNo5(proposalForm.ut)" placeholder="填写需要UT数量"></el-input>
                </el-form-item>
                <el-form-item prop="stage" label="提案分期数" label-width="200px">
                  <el-select v-model="proposalForm.stage" placeholder="填写分期数" popper-class="proposalApplySelect-wrap">
                    <el-option label="1" value="1" class="proposalApplySelect"></el-option>
                    <el-option label="2" value="2" class="proposalApplySelect"></el-option>
                    <el-option label="3" value="3" class="proposalApplySelect"></el-option>
                    <el-option label="4" value="4" class="proposalApplySelect"></el-option>
                    <el-option label="5" value="5" class="proposalApplySelect"></el-option>
                    <el-option label="6" value="6" class="proposalApplySelect"></el-option>
                    <el-option label="7" value="7" class="proposalApplySelect"></el-option>
                    <el-option label="8" value="8" class="proposalApplySelect"></el-option>
                    <el-option label="9" value="9" class="proposalApplySelect"></el-option>
                    <el-option label="10" value="10" class="proposalApplySelect"></el-option>
                    <el-option label="11" value="11" class="proposalApplySelect"></el-option>
                    <el-option label="12" value="12" class="proposalApplySelect"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="5UT转入地址" label-width="200px">
                  <el-input v-model="proposalForm.beneficiaryAddress" placeholder="" class="mainNode-input-large" readonly></el-input>
                </el-form-item>
                <el-form-item prop="transactionID"   label="提案申请5UT交易ID" label-width="200px" maxlength="40">
                  <el-input v-model="proposalForm.transactionID" placeholder="填写交易ID"   @input="checkNo(proposalForm.transactionID)"  maxlength="64" class="mainNode-input-large"></el-input>
                </el-form-item>
                <el-form-item prop="paymentAddress" label="收款/5UT交易地址" label-width="200px">
                  <el-input v-model="proposalForm.paymentAddress"  placeholder="收款地址与5UT交易地址为同一地址" @input="checkNo2(proposalForm.paymentAddress)" class="mainNode-input-large" maxlength="64"></el-input>
                </el-form-item>
                <el-form-item prop="abstract" label="项目简介" label-width="200px" >
                  <el-input v-model="proposalForm.abstract" type="textarea" placeholder="填写项目简介（200字内）" class="mainNode-input-large" maxlength="200"></el-input>
                </el-form-item>

                  <el-form-item prop="fileUrl" required label="项目详情附件">
                  <div class="filename">{{proposalForm.fileName}}</div>
                  <el-upload
                  class="upload"
                  ref="upload"
                  action="https://upload.qiniup.com/"
                  :data = "aaa"
                  :show-file-list="false"
                  :auto-upload="false"  
                   :on-change="handleChangeUpload"
                  :on-success="handleAvatarSuccess"
                  :before-upload="beforeAvatarUpload"
                  :on-progress="uploadFileProcess">
                  <div class="upload-btn">上传附件</div>
                  <span class="fileTip">上传文件只能是zip格式，大小不能超过30MB</span>
                  </el-upload>
                  <el-progress v-if="fileFlag == true" type="circle" :percentage="Number(fileUploadPercent.percentage.toFixed(0))" style="margin-top:30px;"></el-progress>
                  </el-form-item>

                <el-form-item prop="extraUrl" label="项目详情链接">
                  <el-input v-model="proposalForm.extraUrl" placeholder="项目详情链接" class="mainNode-input-large" maxlength="255"></el-input>
                </el-form-item>
                <div class="introduction-box">
                  <el-form-item prop="introTextarea" label="项目介绍">
                    <el-input
                      type="textarea"
                      placeholder="填写项目介绍 （2000字符内）"
                      maxlength="2000"
                      v-model="proposalForm.introTextarea" >
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submit" class="submit-btn">提交提案</el-button>
                  </el-form-item>
                </div>
              </el-form>
          </div>
      </div>
    </div>
    </div>
</template>
<script>
import { submitProposal, checkProposalName, getQiToken } from "@/api/api";
import { getToken } from "@/utils/auth";
import { apiUrl } from "@/api/url";
import {
  isvalidUsername,
  validateNickName3,
  txId,
  validateURL
} from "@/utils/validate";
export default {
  data() {
    const validateName = (rule, value, callback) => {
      if (!value) {
        callback(new Error("提案名不能为空"));
      } else if (value.length > 30) {
        callback(new Error("提案名过长"));
      } else if (!validateNickName3(value)) {
        callback(new Error("请输入正确的提案名"));
      } else if (value && validateNickName3(value)) {
        checkProposalName(value).then(res => {
          if (res.success) {
            callback(new Error("提案名称已存在"));
          } else {
            callback();
          }
        });
      } else {
        callback();
      }
    };
    const validateUt = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入UT所需数"));
      } else if (!this.proposalForm.stage) {
        callback();
      } else if (
        value / this.proposalForm.stage < 500 ||
        value / this.proposalForm.stage > 70000
      ) {
        callback(new Error("UT的范围：500*期数<=需求UT数<=70000*期数"));
      } else {
         this.proposalForm.stage = ''
        this.$refs.proposalForm.validateField("stage", stage => {});
        callback();
      }
    };
    const validatePeriod = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入期数"));
      } else if (!this.proposalForm.ut) {
        callback();
      } else if (
        this.proposalForm.ut / value < 500 ||
        this.proposalForm.ut / value > 70000
      ) {
        callback(new Error("UT的范围：500*期数<=需求UT数<=70000*期数"));
        
      } else {
        callback();
        // this.$refs.proposalForm.validateField("ut", ut => {});
      }
    };
    const validateTxId = (rule, value, callback) => {
      console.log(value);
      if (!value) {
        callback(new Error("请输入交易ID"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的交易id"));
      } else if (value.length != 64) {
        callback(new Error("请输入正确的交易id"));
      } else {
        callback();
      }
    };
    const validateAddress = (rule, value, callback) => {
      console.log(value);
      if (!value) {
        callback(new Error("请输入交易地址"));
      } else if (!txId(value)) {
        callback(new Error("请输入正确的交易地址"));
      } else {
        callback();
      }
    };
    const validateAbstract = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请填写项目简介"));
      } else if (value.length > 200) {
        callback(new Error("项目简介限制50字符内"));
      } else {
        callback();
      }
    };
    const validateContent = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请填写项目介绍"));
      } else if (value.length < 1 || value.length > 2000) {
        callback(new Error("项目简介限制2000字符内"));
      } else {
        callback();
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
      url: apiUrl + "/api/fileOperations/uploadFile.Action",
      fileFlag: false,
      aaa: {},
      headerData: {
        client_name: "jwt",
        token: getToken()
      },
      proposalFormRules: {
        name: [{ required: true, trigger: "blur", validator: validateName }],
        ut: [{ required: true, trigger: "blur", validator: validateUt }],
        stage: [
          { required: true, validator: validatePeriod, trigger: "change" }
        ],
        transactionID: [
          { validator: validateTxId, required: true, trigger: "blur" }
        ],
        paymentAddress: [
          { required: true, trigger: "blur", validator: validateAddress }
        ],
        abstract: [
          { required: true, trigger: "blur", validator: validateAbstract }
        ],
        extraUrl: [{ trigger: "blur", validator: validateExtraUrl }],
        introTextarea: [
          { required: true, trigger: "blur", validator: validateContent }
        ],
        fileUrl: [{ required: true, message: "请上传附件", trigger: "change" }]
      },
      proposalForm: {
        name: "",
        ut: "",
        stage: "",
        beneficiaryAddress: "UkZMxkPhU6Hp9RuqFrdVqKMMSxwvCTxhxQ",
        transactionID: "",
        paymentAddress: "",
        abstract: "",
        introTextarea: "",
        fileName: "",
        fileUrl: "",
        extraUrl: ""
      }
    };
  },
  methods: {
    checkNo(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          console.log("123");
          setTimeout(() => {
            this.proposalForm.transactionID = this.proposalForm.transactionID.replace(
              /\W/g,
              ""
            );
          }, 100);
        }
      }
    },
    checkNo2(value) {
      let reg = /^[1-9]\d*$/;
      if (value) {
        if (value > 999999 || new RegExp(reg).test(value) == false) {
          console.log("123");
          setTimeout(() => {
            this.proposalForm.paymentAddress = this.proposalForm.paymentAddress.replace(
              /\W/g,
              ""
            );
          }, 100);
        }
      }
    },
    checkNo5(value) {
      if (value) {
        setTimeout(() => {
          this.proposalForm.ut = this.proposalForm.ut.replace(/\D/g, "");
        }, 100);
      }
    },
    submit() {
      this.$refs.proposalForm.validate(valid => {
        if (valid) {
          submitProposal(
            this.proposalForm.name,
            this.proposalForm.ut,
            this.proposalForm.stage,
            this.proposalForm.transactionID,
            this.proposalForm.paymentAddress,
            this.proposalForm.abstract,
            this.proposalForm.fileUrl,
            this.proposalForm.extraUrl,
            this.proposalForm.introTextarea
          ).then(res => {
            if (res.success) {
              this.$message({
                message: "提交申请成功",
                type: "success"
              });
              this.$router.push("/personal/myProposal");
            }
          });
        }
      });
    },
    handleAvatarSuccess(res, file) {
      this.proposalForm.fileName = file.name;
      this.proposalForm.fileUrl = res.url + "?attname=" + file.name;
      this.$refs.proposalForm.validateField("fileUrl", fileUrl => {});
    },
    handleChangeUpload(file) {
      getQiToken(file.name).then(res => {
        if (res.success) {
          this.aaa = {
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
    //上传前
    beforeAvatarUpload(file) {
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
    //上传中
    uploadFileProcess(event, file, fileList) {
      this.fileFlag = true;
      this.fileUploadPercent = file;
    }
  }
  //上传成功
};
</script>
<style  rel="stylesheet/scss" lang="scss">
.proposalForm-container {
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
  .el-progress__text {
    font-size: 12px;
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
  // 输入框 start
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
  // 输入框 end

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

  // 提交按钮 start
  .submit-btn {
    background: #4f81f4;
    width: 100px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
    border: none;
    margin-top: 20px;
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
  // 提交按钮 end
}
// 选择下拉框 start
.el-popper .popper__arrow {
  display: none;
}
.el-popper[x-placement^="bottom"] {
  margin-top: 0;
}
.proposalApplySelect-wrap {
  border: none;
  box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.5);
  margin-top: 10px !important;
  .el-select-dropdown__list {
    padding: 0;
  }
  .proposalApplySelect {
    font-size: 14px;
    color: #282828;
    height: 44px;
    line-height: 44px;
    padding: 0 15px !important;
  }
  .proposalApplySelect.selected {
    font-size: 14px;
    color: #d37015;
    font-weight: normal;
    height: 44px;
    line-height: 44px;
  }
  .proposalApplySelect.hover,
  .proposalApplySelect:hover {
    background: #f2f2f2;
    font-size: 14px;
    color: #282828;
    height: 44px;
    line-height: 44px;
  }
}
.el-icon-arrow-up:before {
  content: "\E60C";
  color: #999999;
}
// 选择下拉框 end
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.proposalForm-container {
  padding: 60px 0 100px;
  .upload-btn {
    display: inline-block;
    width: 100px;
    height: 44px;
    font-size: 14px;
    color: #ffffff;
    background: #4f81f4;
    border-radius: 4px;
    margin-right: 10px;
  }
  .container {
    width: 1200px;
    margin: 0 auto;
    background-color: #ffffff;
  }
  .topTitle-wrap {
    position: relative;
    height: 76px;
    line-height: 76px;
    font-size: 18px;
    color: #444444;
    text-align: center;
    border-bottom: 1px solid #eee;
    .topTitle-back {
      position: absolute;
      font-size: 14px;
      color: #d37015;
      right: 30px;
      top: 4px;
    }
  }
  .proposalForm-content-wrap {
    padding-left: 80px;
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 24px 0 40px 0px;
    }
    .proposalForm-box {
      padding-left: 18px;
    }
  }
  .project-introduction-wrap {
    padding-left: 80px;
    border-bottom: 1px solid #eee;
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 24px 0 40px 0px;
    }
    .introduction-box {
      padding-left: 18px;
    }
  }
  .faq-wrap {
    padding-left: 80px;
    padding-bottom: 340px;
    border-bottom: 1px solid #eee;
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 24px 0 40px 0px;
    }
  }
  .filename {
    width: 280px;
    display: inline-block;
    padding: 0 15px;
    border-radius: 4px;
    margin-right: 10px;
    height: 44px;
    line-height: 44px;
    background: #f4f4f4;
    border: 1px solid #dddddd;
    border-radius: 4px;
    font-size: 14px;
    color: #a9a9b3;
  }
  .fileTip {
    font-size: 14px;
    color: #a9a9b3;
    margin: 0 10px;
  }
}
</style>

