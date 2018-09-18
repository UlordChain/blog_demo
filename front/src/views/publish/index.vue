<template>
  <el-row :gutter="20">
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
    <el-col :span="16">
      <div class="grid-content list-home bg-purple">
        <div class="list-header">
          <h3>Ulord博客</h3>
          <router-link to="/info" class="mc info">个人中心</router-link>
          <router-link to="publish" class="mc publish">发布</router-link>
          <router-link to="/" class="mc back">返回主页</router-link>
        </div>
        <div class="list-content">
          <el-form :model="publishForm" :rules="publishFormRules">
            <el-form-item>
              <el-button v-bind:type="btn ? 'default': 'primary'" @click="publishArticle">发布文章</el-button>
              <el-button v-bind:type="!btn ? 'default': 'primary'" @click="publishAd">发布广告</el-button>
            </el-form-item>
            <el-form-item label="文章名">
              <el-input placeholder="文章名" v-model="publishForm.title" maxlength="30"></el-input>
            </el-form-item>
            <el-form-item label="文章简介">
              <el-input type="textarea" placeholder="文章简介" v-model="publishForm.description" maxlength="400"></el-input>
            </el-form-item>
            <div id="editorElem" style="text-align:left"></div>
            <!-- <el-form-item>
                  <el-tag
                  :key="tag"
                  v-for="tag in dynamicTags"
                  closable
                  :disable-transitions="false"
                  @close="handleClose(tag)">
                  {{tag}}
                </el-tag>
                <el-input
                  class="input-new-tag"
                  v-if="inputVisible"
                  v-model="inputValue"
                  ref="saveTagInput"
                  size="small"
                  @keyup.enter.native="handleInputConfirm"
                  @blur="handleInputConfirm"></el-input>
                <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 新增文章标签</el-button>
               </el-form-item> -->
            <el-form-item label="定价">
              <el-input placeholder="定价SUT" type="number" v-model="publishForm.price" maxlength="3"></el-input>
            </el-form-item>
            <el-form-item style="text-align: center">
              <el-button @click.prevent="publish">发布</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-col>
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
  </el-row>
</template>

<script>
import { getToken } from "@/utils/auth";
import E from "wangeditor";
export default {
  data() {
    return {
      data: null,
      data2: null,
      btn: false,
      type: 1,
      token: getToken(),
      editorContent: "",
      dynamicTags: [],
      inputVisible: false,
      inputValue: "",
      publishForm: {
        title: "",
        description: "",
        price: ""
      }
    };
  },
  methods: {
    publish() {
      this.data = Web3Helper.uploadUdfs(
        this.token,
        this.publishForm.title,
        this.publishForm.description,
        this.editorContent
      );
      console.log(this.data);
      if (this.data.result == 1) {
        Web3Helper.publishResource(
          this.token,
          this.data.msg,
          this.publishForm.title,
          this.publishForm.price,
          this.type
        ).then(res => {
          if (res.result == 1) {
            this.$message({
              message: "发布成功",
              type: "success"
            });
            this.$router.push("/");
          }
        });
      }
    },
    publishArticle() {
      this.btn = false;
      this.type = 1;
    },
    publishAd() {
      this.btn = true;
      this.type = 2;
    },
    // getContent: function() {
    //   alert(this.editorContent);
    // },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    }
  },
  mounted() {
    var editor = new E("#editorElem");
    editor.customConfig.onchange = html => {
      this.editorContent = html;
    };
    editor.customConfig.uploadImgShowBase64 = true;
    editor.create();
  }
};
</script>


<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #fff;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}

.list-home {
  .list-header {
    position: relative;
    h3 {
      display: inline-block;
    }
  }
  .mc {
    padding: 10px;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  .info {
    right: 0px;
  }
  .publish {
    right: 90px;
  }
  .back {
    right: 153px;
  }
}
</style>
