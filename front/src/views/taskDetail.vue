<template>
  <div class="bountyMissions-container" v-if="!loading">
    <div class="header-wrap">
      <top-Header></top-Header>
  </div>
    <div class="container">
      <!-- 申请任务 start -->
      <div class="bountyMissions">
         <div class="topTitle-wrap">
           <h4>{{data.bountyTaskName}}</h4>
           <p>
             赏金<span>{{data.reward}}UT</span>
            </p>
         </div>
         <div class="table-wrap">
            <table>
                <tbody>
                  <tr>
                    <td class="table-name">任务描述</td>
                    <td class="table-content">{{data.requirementDesc}}</td>
                  </tr>
                  <tr>
                    <td class="table-name">开发周期</td>
                    <td class="table-content">{{data.devData}} 天</td>
                  </tr>
                  <tr>
                    <td class="table-name">开发工作量</td>
                    <td class="table-content">{{data.devWorkload}} 人/月</td>
                  </tr>
                  <tr class="large-box">
                    <td class="table-name">参考文献</td>
                    <td class="table-content">
                       <ul class="explain-list">
                        <li>
                          {{data.referenceDocumentation}}
                          <!-- <span>官方支持</span>
                          <router-link to="https://github.com/UlordChain/ulord-blog-demo" class="table-link">
                            https://github.com/UlordChain/ulord-blog-demo
                          </router-link>
                        </li>
                        <li>
                          <span>开发文档</span>
                          <router-link to="https://github.com/UlordChain/ulord-blog-demo" class="table-link">
                            开发环境
                          </router-link> -->
                        </li>
                      </ul>
                    </td>
                  </tr>
                  <tr class="large-box">
                    <td class="table-name">需求说明</td>
                    <td class="table-content ">
                      <ul class="explain-list">
                        <li>{{data.requirementDesc}}</li>
                        <!-- <a :href="requireUrl" class="download">下载需求文档</a> -->
                      </ul>
                    </td>
                  </tr>
                </tbody>
            </table>
            <!-- <div v-if="this.$route.query.taskStatus == 0">
              <el-button type="primary" @click.prevent.native="apply" class="submit-btn">申请任务</el-button>
            </div> -->
            <div v-if="this.$route.query.taskStatus == 1" class="devReport">
              <h4>开发进度报告</h4>
              <div v-for="pro in taskRateDos" :key="pro.index">
                <p>
                  {{pro.description}}
                </p>
                <span>{{pro.gmtModify | timeDay}}</span>
              </div>
              <el-form :model="taskProgressForm" ref="taskProgressForm" :rules="taskProgressFormRules" v-if="this.$route.query.userId == mineId" >
                <el-form-item prop="taskDes">
                  <el-input
                    type="textarea"
                    placeholder="开发进度报告"
                    maxlength="2000"
                    v-model="taskProgressForm.taskDes">
                  </el-input>
                </el-form-item>
                 <el-button @click.prevent.native="submit" class="submit" type="primary">提交开发进度报告</el-button>
              </el-form>
            </div>
            <div v-else-if="this.$route.query.taskStatus == 2" class="submit-btn-wrap">
              该任务已结束
            </div>
            <div v-else-if="this.$route.query.taskStatus == 4" class="submit-btn-wrap">
              您的申请已提交，正在评选中。
            </div>
            <template v-else>
              <div class="submit-btn-wrap" v-if="status == -1">
                 <div v-if="Boolean((data.putawayShowTime + data.gmtPutaway - Math.floor((new Date()).getTime() / 1000)) < 0)">该任务已过方案提交时间，目前正在进行方案评审</div>
                  <el-button v-else type="primary" @click.prevent.native="apply(data.isOpenSource)" class="submit-btn">申请任务</el-button>
              </div>
              <div class="submit-btn-wrap" v-if="status == 4">
                 <div>您的申请已提交，正在评选中。</div>
              </div>
            </template>
         </div>
      </div>
      <!-- 申请任务 end -->
      <!-- 状态 start -->
      <div class="bountyMissions-state">
          <h4>
            <i class="el-icon-circle-check"></i>
            方案提交成功
          </h4>
          <p>评审结果将以短信的形式通知你，请耐心等待。</p>
          <router-link to="/" class="backHome">返回开发者</router-link>
      </div>
      <!-- 状态 end -->
    </div>
  </div>
</template>

<script>
import {
  getTaskDetail,
  getCompletedTaskDt,
  getTaskApplyStats,
  submitTaskProgress
} from "@/api/api";
import axios from "axios";
import { getId } from "@/utils/auth";
import store from "../store";
import { apiUrl } from "@/api/url";
import { getToken } from "@/utils/auth";
export default {
  data() {
    const validateDes = (rule, value, callback) => {
      if (!value) {
        callback(new Error("请输入开发进度报告"));
      } else {
        callback();
      }
    };
    return {
      data: null,
      api: apiUrl,
      loading: true,
      status: -1,
      requireUrl: "",
      isReal: store.getters.real,
      taskRateDos: [],
      taskProgressForm: {
        taskDes: ""
      },
      mineId: getId(),
      taskProgressFormRules: {
        taskDes: [{ required: true, trigger: "blur", validator: validateDes }]
      }
    };
  },
  methods: {
    taskDetail(id) {
      var that = this;
      that.loading = true;
      axios.all([getTaskDetail(id), getTaskApplyStats(id)]).then(
        axios.spread(function(detail, status) {
          that.data = detail.bountyTaskDetailsDo;
          that.requireUrl = detail.bountyTaskDetailsDo.requirementDoc;
          that.status = status.appliedStatus;
          that.loading = false;
        })
      );
    },
    taskingDetail(id) {
      var that = this;
      that.loading = true;
      that.taskProgressForm.taskDes = "";
      axios.all([getTaskDetail(id), getCompletedTaskDt(id)]).then(
        axios.spread(function(detail, status) {
          that.data = detail.bountyTaskDetailsDo;
          that.taskRateDos = status.taskRateDos;
          that.status = status.appliedStatus;
          that.loading = false;
        })
      );
    },
    submit() {
      this.$refs.taskProgressForm.validate(valid => {
        if (valid) {
          submitTaskProgress(
            this.taskProgressForm.taskDes,
            this.$route.query.id
          ).then(res => {
            if (res.success) {
              this.$message({
                message: "提交成功",
                type: "success"
              });
              this.taskingDetail(this.$route.query.id);
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    apply(isOpenSource) {
      if (!store.getters.real) {
        this.$confirm("您还未进行实名认证", "提示", {
          confirmButtonText: "去认证",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            this.$router.push("/personal/realNameAuth");
          })
          .catch(() => {});
      } else {
        this.$router.push({
          path: "/taskApply/",
          query: { id: this.$route.query.id, isOpenSource: isOpenSource }
        });
      }
    }
  },
  mounted() {
    if (this.$route.query.taskStatus == 0) {
      this.taskDetail(this.$route.query.id);
    } else {
      this.taskingDetail(this.$route.query.id);
    }
  }
};
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
.bountyMissions-container {
  padding: 55px 0;
  .download {
    float: right;
    display: inline-block;
    width: 90px;
    height: 26px;
    line-height: 26px;
    border-radius: 4px;
    background-color: #4f81f4;
    color: #fff;
    padding: 8px 12px;
  }
  .container {
    width: 1200px;
    margin: 0 auto;
  }
  /*====================================
           赏金任务申请
  =====================================*/
  .devReport {
    h4 {
      font-size: 18px;
      margin-bottom: 6px;
    }
    .submit {
      margin-top: 8px;
      float: right;
    }
    margin: 40px 48px 40px 52px;
    & > div {
      position: relative;
      min-height: 40px;
      border: 1px solid #ebebeb;
      margin-bottom: 20px;
      padding: 8px;
      span {
        position: absolute;
        bottom: 6px;
        right: 6px;
      }
    }
  }
  .bountyMissions-state {
    display: none;
  }
  .topTitle-wrap {
    margin-top: 40px;
    position: relative;
    height: 126px;
    color: #ffffff;
    text-align: center;
    background-image: linear-gradient(-90deg, #05e3d4 7%, #4f81f4 93%);
    h4 {
      font-size: 24px;
      padding: 22px 0 15px;
    }
    p {
      font-size: 24px;
      line-height: 36px;
      span {
        font-weight: bold;
        margin-left: 20px;
      }
    }
  }
  // 表格布局 start
  .table-wrap {
    table {
      width: 100%;
      margin: 40px 0 40px 0;
      border-collapse: collapse;
    }
    td {
      background: #ffffff;
      border: 1px solid #ebebeb;
      box-sizing: border-box;
      vertical-align: top;
      p {
        font-size: 14px;
        color: #666666;
        text-align: justify;
        line-height: 24px;
      }
    }
    .table-name {
      width: 20%;
      min-height: 60px;
      padding-left: 60px;
      font-size: 16px;
      color: #444444;
      padding: 23px 61px;
    }
    .table-content {
      width: 80%;
      min-height: 60px;
      padding: 23px 61px;
      font-size: 14px;
      color: #666666;
      .explain-list {
        li {
          margin-bottom: 14px;
          &::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4f81f4;
            display: inline-block;
            margin-right: 10px;
          }
          &:last-child {
            margin-bottom: 0;
          }
          span {
            font-size: 14px;
            color: #666666;
            margin-right: 20px;
          }
        }
      }
      .word-count {
        font-size: 14px;
        color: #666666;
        text-align: right;
        line-height: 24px;
        .used {
          color: #3f3f3f;
        }
        .total {
          font-size: 14px;
          color: #666666;
        }
      }
    }
    .table-link {
      font-size: 14px;
      color: #4f81f4;
    }
    .large-box td {
      vertical-align: top;
      padding-top: 20px;
      padding-bottom: 20px;
    }
  }
  // 表格布局 end
  // 提交按钮 start
  .submit-btn-wrap {
    margin: 0 auto;
    text-align: center;
  }
  .submit-btn {
    background: #4f81f4;
    width: 230px;
    height: 50px;
    line-height: 50px;
    padding: 0;
    font-size: 18px;
    color: #ffffff;
    border: none;
  }

  .icon-check {
    font-size: 24px;
    color: #6bc00c;
    vertical-align: sub;
  }
  .check-tip {
    font-size: 16px;
    color: #666666;
    vertical-align: middle;
  }
  /*====================================
           申请反馈
    =====================================*/
  .bountyMissions-state {
    margin: 40px auto;
    height: 480px;
    background: #ffffff;
    box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.5);
    border-radius: 4px;
    text-align: center;
    h4 {
      font-size: 20px;
      color: #444444;
      padding-top: 112px;
      i {
        font-size: 24px;
        display: inline-block;
        color: #6bc00c;
        vertical-align: text-bottom;
      }
    }
    p {
      font-size: 16px;
      color: #666666;
      margin: 28px 0 50px;
    }
    .backHome {
      font-size: 14px;
      color: #d37015;
    }
  }
  .taskRateDos {
    font-size: 16px;
    color: #666666;
    line-height: 32px;
    padding: 0 60px;
    margin-bottom: 40px;
  }
}
</style>
