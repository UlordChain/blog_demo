<template>
  <div class="task-container">
    <div v-if="!loading">
      <ul class="task-list" v-if="myTaskList.length !== 0">
        <li v-for="item in myTaskList" :key="item.index" >
          <div class="task-state-wrap">
              <h4>{{item.bountyTaskName}}</h4>
            <span>{{item.status | statusTrans}}</span>
          </div>
          <div class="task-report-wrap">

            <p>{{item.bountyTaskDesc}}</p>
            <el-button v-if="item.status == 1" type="primary" @click="go(item.status, item.bountyTaskId, userId)" class="submit-btn">提交进度报告</el-button>
            <el-button v-if="item.status == 0" type="primary" @click="go(item.status, item.bountyTaskId)" class="submit-btn">查看任务</el-button>
            <el-button v-if="item.status == 2" type="primary" @click="go(item.status, item.bountyTaskId, userId)" class="submit-btn">查看任务</el-button>
            <el-button v-if="item.status == 4" type="primary" @click="go(item.status, item.bountyTaskId)" class="submit-btn">查看任务</el-button>
          </div>
        </li>
      </ul>
      <div v-else>
        <div class="noTask-container">
            <div class="noTask-bg"></div>
            <p>哎呦，你还没有做过任务诶</p>
            <el-button type="primary" class="search-btn" @click="goOther">看看别人的</el-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { myTask } from "@/api/api";
import { getId } from "@/utils/auth";
export default {
  data() {
    return {
      myTaskList: [],
      loading: true,
      userId: getId()
    };
  },
  filters: {
    statusTrans(value) {
      if (value == 0) {
        return "方案未被选中";
      } else if (value == 1) {
        return "开发中";
      } else if (value == 2) {
        return "任务失败";
      } else if (value == 3) {
        return "任务成功";
      } else if (value == 4) {
        return "方案评选中";
      }
    }
  },
  beforeCreate() {
    document.querySelector("body").setAttribute("style", "background:#f4f4f4");
  },
  beforeDestroy() {
    document.querySelector("body").setAttribute("style", "");
  },
  methods: {
    getTask() {
      var that = this;
      const loading = this.$loading({
        lock: true,
        text: "加载中",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0)",
        target: document.querySelector(".main-container")
      });
      that.loading = true;
      myTask(1, 10, 5).then(function(res) {
        that.myTaskList = res.userTaskDos;
        loading.close();
        that.loading = false;
      });
    },
    go(status, bountyTaskId, receiveId) {
      this.$router.push({
        path: "/taskDetail/",
        query: { id: bountyTaskId, userId: receiveId, taskStatus: status }
      });
    },
    goOther() {
      this.$router.push({ path: "/" });
    }
  },
  mounted() {
    this.getTask();
  }
};
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
body {
  background-color: #f4f4f4;
}
.main-container {
  padding: 0 !important;
}
.task-container {
  padding-bottom: 200px;
  .task-list {
    li {
      height: 140px;
      margin: 0 30px;
      border-bottom: 1px solid #eee;
      .task-state-wrap {
        margin-bottom: 24px;
        padding-top: 31px;
        h4 {
          font-size: 16px;
          color: #444444;
          display: inline-block;
        }
        span {
          font-size: 14px;
          color: #444444;
          display: inline-block;
          margin-right: 30px;
          float: right;
        }
      }

      .task-report-wrap {
        clear: both;
        p {
          font-size: 14px;
          color: #666666;
          width: 480px;
          height: 40px;
          display: inline-block;
          overflow: hidden;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          /*! autoprefixer: off */
          -webkit-box-orient: vertical;
          /* autoprefixer: on */
          float: left;
        }
        // 提交按钮 start
        .submit-btn {
          background: #4f81f4;
          width: 168px;
          height: 44px;
          line-height: 44px;
          padding: 0;
          font-size: 14px;
          color: #ffffff;
          float: right;
          margin-right: 30px;
          border: none;
        }
        .el-button--primary:focus,
        .el-button--primary:hover {
          background: #4f81f4;
          width: 168px;
          height: 44px;
          line-height: 44px;
          padding: 0;
          font-size: 14px;
          color: #ffffff;
        }
        // 提交按钮 end
      }
    }
    .state-await,
    .state-over {
      .task-state-wrap {
        span {
          font-size: 14px;
          color: #999999;
        }
      }
    }
  }
}
.noTask-container {
  margin: 0 auto;
  text-align: center;
  .noTask-bg {
    width: 134px;
    height: 160px;
    background: url(../assets/myTask-bg.png) no-repeat center;
    margin: 40px auto 0;
  }
  p {
    font-size: 18px;
    color: #666666;
    margin: 40px auto;
  }
  .search-btn {
    background: #4f81f4;
    width: 120px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
  }
  .search-btn.el-button--primary:focus,
  .el-button--primary:hover {
    background: #4f81f4;
    width: 120px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
  }
  .el-button {
    border: none;
  }
}
</style>

