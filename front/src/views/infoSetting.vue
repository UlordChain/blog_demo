<template>
  <div class="infoSetting-container">
    <div class="container">
      <h1 class="title">
        设置个人资料
      </h1>
      <el-upload
        class="avatar-uploader"
        ref="upload"
        action="https://upload.qiniup.com/"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :data = "uploadData"
        :auto-upload="false"   
        :on-change="handleChangeUpload"
        :before-upload="beforeAvatarUpload">
        <img v-if="imageUrl" :src="imageUrl" class="avatar">
        <div class="upload-bg">修改</div>
      </el-upload>
      <el-form class="infoSetting-form-wrap">
        <el-form-item prop="username" class="gender-wrap">
        <span class="name">性别</span>
          <el-radio-group v-model="radio2">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="2">女</el-radio>
            <el-radio :label="0">保密</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item class="choice-wrap">
          <div class="block">
            <span class="demonstration name">城市</span>
            <el-cascader
              :options="options2"
              v-model="selectedOptions2"
              placeholder = "请选择"
              @change="handleChange2"
              popper-class = "city">
            </el-cascader>
          </div>
        </el-form-item>
        <el-form-item>
          <div class="block">
            <span class="demonstration name">行业</span>
            <el-cascader
              :options="options"
              v-model="selectedOptions"
              placeholder = "请选择"
              @change="handleChange"
              popper-class = "city">
            </el-cascader>
          </div>
        </el-form-item>
        <el-form-item class="submit-btn-wrap">
          <el-button type="primary"  @click.native.prevent="saveModify" class="submit-btn">保存</el-button>
            <el-button type="primary"  @click.native.prevent="saveModify2" class="submit-btn">跳过</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import { getToken, getId } from "@/utils/auth";
import { verify, getQiToken } from "@/api/api";
import industry from "@/components/industry";
import city from "@/components/city";
import { apiUrl } from "@/api/url";
import store from "../store";

export default {
  data() {
    return {
      radio2: 0,
      imageUrl: "https://xuanwuyun.com/FnDqL6spdWrhf7_6d1gRGNsc5RMU",
      uploadUrl:
        store.getters.avatar ||
        "https://xuanwuyun.com/FnDqL6spdWrhf7_6d1gRGNsc5RMU",
      uploadData: {},
      userid: getId(),
      options: industry,
      selectedOptions: [],
      options2: city,
      selectedOptions2: []
    };
  },
  methods: {
    saveModify2() {
      this.$router.push({ path: "/" });
    },
    handleChange(value) {},
    handleChange2(value) {},
    saveModify() {
      verify(
        this.uploadUrl,
        this.selectedOptions2.join("-"),
        this.selectedOptions.join("-"),
        this.radio2,
        this.userid
      ).then(res => {
        if (res.data.errorCode == "OK") {
          this.$message({
            message: "设置成功",
            type: "success"
          });
          this.$router.push({ path: "/" });
        }
      });
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = res.url;
      this.uploadUrl = res.url;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG和PNG 格式!");
        return false;
      } else if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
        return false;
      } else {
        return true;
      }
      // else {
      //   return getQiToken(file.name).then(res => {
      //     this.uploadData = {
      //       token: res.token
      //     };
      //   });
      // }
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
    }
  }
};
</script>
<style rel="stylesheet/scss" lang="scss">
body {
  background: #fff;
}
.infoSetting-container {
  .upload-bg {
    position: absolute;
    width: 120px;
    height: 120px;
    line-height: 120px;
    top: 0;
    color: #fff;
    background-color: rgba(0, 0, 0, 0.2);
  }
  .avatar-uploader {
    margin: 47px auto 23px;
    .el-upload {
      border: 1px solid #d9d9d9;
      border-radius: 50%;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      background-color: rgba(0, 0, 0, 0.2);
      &:hover {
        border-color: #4f81f4;
      }
    }
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 120px;
    height: 120px;
    line-height: 120px;
    text-align: center;
  }
  .avatar {
    width: 120px;
    height: 120px;
    display: block;
  }

  .infoSetting-form-wrap {
    // 单选按钮 start
    .gender-wrap {
      .el-radio {
        font-size: 18px;
        color: #444444;
      }
      .el-radio__label {
        font-size: 14px;
        color: #999999;
      }
      .el-radio__inner {
        width: 16px;
        height: 16px;
        background: #ffffff;
        border: 1px solid #979797;
      }
      .el-radio__input.is-checked .el-radio__inner {
        background: transparent;
        border-color: #979797;
      }
      .el-radio__inner::after {
        width: 10px;
        height: 10px;
        background: #4f81f4;
      }
      .el-radio-group {
        width: 280px;
        line-height: 44px;
      }
      .el-radio {
        line-height: 44px;
      }
    }
    // 单选按钮 end

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
      border: none;
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
    .el-icon-arrow-down:before {
      content: "\E60B";
    }
    // 输入框 end
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
      margin-top: 45px;
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
}

// 级联选择器 start
.choice-wrap {
  .el-cascader__label {
    font-size: 14px;
    color: #a9a9b3;
  }
}
.city {
  .el-cascader {
    width: 280px;
    line-height: 44px;
  }
  .el-input__inner {
    font-size: 14px;
    color: #666666;
    height: 44px;
    line-height: 44px;
  }
  .el-cascader-menu__item--extensible:after {
    right: 4px;
  }
  .el-cascader__label {
    font-size: 14px;
    color: #666666;
  }
  .el-cascader-menu__item.is-active {
    font-size: 14px;
    color: #d37015;
  }
  .el-cascader-menu__item:focus:not(:active),
  .el-cascader-menu__item:hover {
    background: #f2f2f2;
  }
  .el-cascader-menu__item {
    font-size: 14px;
    color: #282828;
    height: 40px;
    line-height: 1.5;
  }
}
// 级联选择器 end
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.infoSetting-container {
  text-align: center;
  margin-bottom: 70px;
  padding-top: 54px;
  .container {
    width: 1200px;
    margin: 0 auto;
  }
  .title {
    font-size: 24px;
    color: #444444;
    text-align: center;
    line-height: 120px;
  }
  .el-form-item .name {
    width: 55px;
    display: inline-block;
    text-align: left;
    font-size: 14px;
    color: #999999;
  }
  .info-img {
    width: 120px;
    height: 120px;
    background: url(./../assets/timg.jpg) no-repeat center;
    border-radius: 50%;
    background-size: 120px;
    margin: 0px auto;
  }
  .nickName {
    display: inline-block;
    vertical-align: text-bottom;
    font-size: 16px;
    color: #444444;
    margin-top: 20px;
  }
  .modify {
    display: inline-block;
    vertical-align: text-bottom;
    font-size: 14px;
    color: #d37015;
    margin-top: 20px;
    box-sizing: border-box;
    margin-left: 22px;
    cursor: pointer;
  }
}
</style>

