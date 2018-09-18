<template>
  <div class="info-wrap myinfo">
    <el-upload
    ref="upload"
      :disabled="!isModify"
      class="avatar-uploader"
      action="https://upload.qiniup.com/"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :data = "uploadData"
       :auto-upload="false"   
      :on-change="handleChangeUpload"
      :before-upload="beforeAvatarUpload">
      <img v-if="imageUrl" :src="imageUrl" class="avatar">
      <div v-show="isModify" class="upload-bg">修改</div>
    </el-upload>
    <div class="modify" @click="modify" v-show="!isModify">修改</div>
    <el-form>
      <el-form-item prop="username">
        <span class="name">昵称</span>
        <el-input v-model="nickName" readonly class="nickname-input"></el-input>
      </el-form-item>
      <el-form-item prop="username">
       <span class="name">性别</span>
        <el-radio-group v-model="radio2" :disabled="!isModify">
          <el-radio :label="1">男</el-radio>
          <el-radio :label="2">女</el-radio>
          <el-radio :label="0">保密</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <div class="block">
          <span class="demonstration name">城市</span>
          <el-cascader
            :disabled = "!isModify"
            :options="options2"
            v-model="selectedOptions2"
            placeholder = "请选择"
            @change="handleChange2"
            popper-class="cascader-wrap"
            >
          </el-cascader>
        </div>
      </el-form-item>
      <el-form-item>
        <div class="block">
          <span class="demonstration name">行业</span>
          <el-cascader
            :disabled = "!isModify"
            :options="options"
            v-model="selectedOptions"
            placeholder = "请选择"
            @change="handleChange"
            class="cascader-checked"
             popper-class="cascader-wrap">
          </el-cascader>
        </div>
      </el-form-item>
       <el-form-item>
         <el-button type="primary" v-show="isModify" @click.native.prevent="saveModify" class="save-btn">保存</el-button>
         <el-button type="primary" v-show="isModify" @click.native.prevent="saveModify2" class="cancel-btn">取消</el-button>
       </el-form-item>
    </el-form>

  </div>
</template>
<script>
import { getToken, getId } from "@/utils/auth";
import { verify, getInfo2, getQiToken } from "@/api/api";
import industry from "@/components/industry";
import city from "@/components/city";
import { apiUrl } from "@/api/url";
import store from "../store";
export default {
  data() {
    return {
      url: apiUrl + "/api/fileOperations/uploadFile.Action",
      radio2: 0,
      isModify: false,
      imageUrl: store.getters.avatar,
      uploadUrl: store.getters.avatar,
      uploadData: {},
      headerData: {
        client_name: "jwt",
        token: getToken()
      },
      nickName: "",
      options: industry,
      selectedOptions: [],
      options2: city,
      selectedOptions2: []
    };
  },
  methods: {
    saveModify2() {
      this.isModify = false;
    },
    handleChange(value) {
      console.log(value);
    },
    getInformation() {
      getInfo2().then(res => {
        console.log(res);
        this.nickName = res.data.result.displayName;
        this.radio2 = res.data.result.sex;
        if (res.data.result.hasOwnProperty("city")) {
          this.selectedOptions2 = res.data.result.city.split("-");
        } else {
          this.selectedOptions2 = [];
        }
        if (res.data.result.hasOwnProperty("industries")) {
          this.selectedOptions = res.data.result.industries.split("-");
        } else {
          this.selectedOptions = [];
        }
      });
    },
    handleChange2(value) {
      console.log(value);
    },
    modify() {
      this.isModify = !this.isModify;
      console.log(this.isModify);
    },
    saveModify() {
      verify(
        this.uploadUrl,
        this.selectedOptions2.join("-"),
        this.selectedOptions.join("-"),
        this.radio2,
        getId()
      ).then(res => {
        if (res.data.errorCode == "OK") {
          console.log("222", res);
          this.$message({
            message: "修改成功",
            type: "success"
          });
          location.reload();
        }
      });
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
    handleAvatarSuccess(res, file) {
      this.uploadUrl = res.url;
      this.imageUrl = res.url;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg" || file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG和PNG 格式!");
        return false;
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
        return false;
      }
    }
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  },
  mounted() {
    this.getInformation();
  }
};
</script>
<style rel="stylesheet/scss" lang="scss">
.info-wrap {
  .myinfo .el-input {
    width: 280px;
  }
  .myinfo .el-upload {
    position: relative;
  }
  .myinfo .avatar-uploader {
    margin-bottom: 20px;
  }
  .el-input__inner {
    font-size: 14px;
    color: #666666;
    width: 280px;
    height: 44px;
    line-height: 44px;
    background: #f4f4f4;
    border: 1px solid #dddddd;
    border-radius: 4px;
    display: inline-block;
  }

  .nickname-input {
    font-size: 14px;
    color: #666666;
    width: 280px;
    height: 44px;
    line-height: 44px;
    background: #f4f4f4;
    border: none;
    border-radius: 4px;
    display: inline-block;
  }
  .nickname-input .el-input__inner {
    font-size: 14px;
    color: #a9a9b3;
    background: #f4f4f4;
    border-radius: 4px;
    border-color: transparent;
  }
  .nickname-input .el-input.is-active .el-input__inner,
  .el-input__inner:focus {
    border-color: transparent;
    outline: 0;
  }
  // 单选按钮 start
  .el-radio-group {
    width: 280px;
  }
  .el-radio {
    font-size: 18px;
    color: #444444;
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
  // 单选按钮 end
}

// 级联选择器 start
.cascader-wrap {
  width: 280px;
  line-height: 44px;
}
.cascader-wrap .el-cascader-menu__item--extensible:after {
  right: 4px;
}
.cascader-wrap .el-cascader-menu__item {
  font-size: 14px;
  color: #282828;
  height: 40px;
}
.cascader-wrap .el-cascader-menu__item.is-active {
  font-size: 14px;
  color: #d37015;
}
.cascader-wrap .el-cascader-menu__item:focus:not(:active),
.cascader-wrap .el-cascader-menu__item:hover {
  background: #f2f2f2;
}
.cascader-wrap .el-cascader__label {
  font-size: 14px;
  color: #666666;
}
.el-cascader.is-disabled .el-cascader__label {
  background: #f4f4f4;
  border-radius: 4px;
  font-size: 14px;
  color: #666666;
  border: 1px solid #dddddd;
}
.cascader-checked {
  background: #f4f4f4;
  border-radius: 4px;
  font-size: 14px;
  color: #666666;
}

// 级联选择器 end
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.info-wrap {
  text-align: center;
  margin-bottom: 70px;
  .upload-bg {
    position: absolute;
    width: 120px;
    height: 120px;
    top: 0;
    line-height: 120px;
    color: #fff;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.2);
    margin-top: 30px;
  }
  .el-form-item .name {
    width: 55px;
    display: inline-block;
    text-align: left;
    font-size: 14px;
    color: #999999;
  }

  .save-btn {
    width: 120px;
    height: 44px;
    background: #4f81f4;
    border-radius: 4px;
    &:hover {
      background: #4f81f4;
      border-color: #4f81f4;
      color: #fff;
    }
  }
  .cancel-btn {
    width: 120px;
    height: 44px;
    background: #4f81f4;
    border-radius: 4px;
    &:hover {
      background: #4f81f4;
      border-color: #4f81f4;
      color: #fff;
    }
  }
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
  margin: 0 0 20px;
  box-sizing: border-box;
  cursor: pointer;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
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
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
  border-radius: 50%;
}
.avatar {
  width: 120px;
  height: 120px;
  display: block;
  border-radius: 50%;
  margin-top: 30px;
  margin-bottom: 23px;
}
</style>

