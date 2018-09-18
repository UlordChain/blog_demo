<template>
  <div class="my-proposal-container">
     <el-button  @click="goApply" class="submit-btn">提交申请</el-button>
     <el-tabs v-model="activeName" @tab-click="handleClick" class="myProposal-tabs-wrap">

       <!-- 全部提案 -->
        <el-tab-pane label="全部提案" name="first">
          <div v-if="!loading">
          <ul v-if="proposalList.length !== 0" class="proposal-content" >
            <li v-for="item in proposalList" :key="item.index">
              <div class="proposal-content-lf">
                 <router-link :to="{path:'/proposalDetail', query:{id: item.proposalId, name: item.displayName, status: item.periodStatus}}">
                   <h4>{{item.proposalName}}</h4>
                    <p>{{item.digest}}</p>
                 </router-link>
              </div>
              <div class="proposal-content-rt">
                <el-progress :percentage="item.voteNumYes | progress(data.majorNodeCount)"></el-progress>
                <p v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">投票统计中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">未通过</p>
                <p v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">投票中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">未通过</p>
              </div>
            </li>
          </ul>
           <div v-else>
            <div class="noTask-container">
              <div class="noTask-bg"></div>
              <p>哎呦，还没有提案诶</p>
              <el-button type="primary" class="search-btn" @click="goOther">看看别人的</el-button>
            </div>
           </div>
           </div>
        </el-tab-pane>
        <!-- 投票中 -->
        <el-tab-pane label="投票中" name="second">
          <div v-if="!loading">
            <ul v-if="proposalList.length !== 0" class="proposal-content">
            <li  v-for="item in proposalList" :key="item.index">
              <div class="proposal-content-lf">
                <router-link :to="{path:'/proposalDetail', query:{id: item.proposalId, name: item.displayName, status: item.periodStatus}}">
                   <h4>{{item.proposalName}}</h4>
                    <p>{{item.digest}}</p>
                 </router-link>
              </div>
              <div class="proposal-content-rt">
               <el-progress :percentage="item.voteNumYes | progress(data.majorNodeCount)"></el-progress>
                <p v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">投票统计中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">未通过</p>
                <p v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">投票中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">未通过</p>
              </div>
            </li>
          </ul>
           <div v-else>
               <div class="noTask-container">
              <div class="noTask-bg"></div>
              <p>哎呦，还没有提案诶</p>
              <el-button type="primary" class="search-btn" @click="goOther">看看别人的</el-button>
            </div>
           </div>
          </div>
        </el-tab-pane>
        <!-- 已完成 -->
        <el-tab-pane label="已完成" name="third">
          <div v-if="!loading">
          <ul v-if="proposalList.length !== 0" class="proposal-content">
            <li  v-for="item in proposalList" :key="item.index">
              <div class="proposal-content-lf">
                <router-link :to="{path:'/proposalDetail', query:{id: item.proposalId, name: item.displayName, status: item.periodStatus}}">
                   <h4>{{item.proposalName}}</h4>
                    <p>{{item.digest}}</p>
                 </router-link>
              </div>
              <div class="proposal-content-rt">
                <el-progress :percentage="item.voteNumYes | progress(data.majorNodeCount)"></el-progress>
                <p v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">投票统计中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">未通过</p>
                <p v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">投票中</p>
                <p v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">已通过</p>
                <p v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">未通过</p>
              </div>
            </li>
          </ul>
          <div v-else>
            <div class="noTask-container">
            <div class="noTask-bg"></div>
            <p>哎呦，还没有提案诶</p>
            <el-button type="primary" class="search-btn" @click="goOther">看看别人的</el-button>
          </div>
        </div>
           </div>
        </el-tab-pane>
     </el-tabs>
  </div>
</template>
<script>
import navBar from "../components/navbar.vue";
import { getUserAllProposal } from "@/api/api";
import store from "../store";
export default {
  data() {
    return {
      data: null,
      value: "",
      activeName: "first",
      proposalList: [],
      loading: true,
      per: 0
    };
  },
  filters: {
    progress(value, acount) {
      if (acount == 0) {
        return 0;
      } else {
        return Math.floor(value / acount * 100);
      }
    },
    pp(value) {
      if (value == 0) {
        return "投票中";
      } else if (value == 1) {
        return "已通过";
      } else if (value == 2) {
        return "未通过";
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
    goOther() {
      this.$router.push("/proposal");
    },
    goApply() {
      if (!store.getters.real) {
        this.$message({
          message: "请先进行实名认证",
          type: "error"
        });
        return;
      }
      this.$router.push({ path: "/proposalApply" });
    },
    handleClick(tab, event) {
      this.getList(tab.index, 10, 1);
    },
    getList(searchType, pageSize, pageNumber) {
      this.loading = true;
      const loading = this.$loading({
        lock: true,
        text: "加载中",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0)",
        target: document.querySelector(".main-container")
      });
      this.loading = true;
      getUserAllProposal(searchType, pageSize, pageNumber).then(res => {
        this.data = res;
        this.proposalList = res.proposalDoList;
        loading.close();
        this.loading = false;
      });
    }
  },
  mounted() {
    this.getList(0, 10, 1);
  }
};
</script>
<style rel="stylesheet/scss" lang="scss" >
.my-proposal-container {
  .el-tabs__item {
    height: 80px;
    line-height: 80px;
  }
  // 切换 start
  .myProposal-tabs-wrap {
    .el-tabs__content {
      overflow: visible;
    }
    .el-tabs__item {
      padding: 0 40px;
      height: 76px;
      line-height: 76px;
      font-size: 16px;
      color: #a9a9b3;
      text-align: center;
    }
    .el-tabs--top .el-tabs__item.is-top:last-child {
      padding: 0 20px 0 40px;
    }

    .el-tabs__active-bar {
      background-color: #4f81f4;
    }
    .el-tabs__item.is-active {
      font-size: 18px;
      color: #444444;
    }
    .el-tabs__nav {
      float: left;
    }
    .el-tabs__nav-wrap::after {
      height: 1px;
      background-color: #eeeeee;
    }
  }
  .el-tabs--top .el-tabs__item.is-top:nth-child(2) {
    padding: 0 40px 0 20px;
  }
  // 切换 end
  .el-progress-bar__outer {
    width: 120px;
    height: 20px !important;
  }
  .el-progress__text {
    display: none;
  }
  .el-progress-bar__inner {
    background-color: #4f81f4;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.main-container {
  padding: 0 !important;
}
.my-proposal-container {
  position: relative;

  .submit-btn {
    background: #4f81f4;
    width: 100px;
    height: 44px;
    line-height: 44px;
    padding: 0;
    font-size: 14px;
    color: #ffffff;
    border-color: #4f81f4;
    position: absolute;
    top: 16px;
    right: 10px;
    border-radius: 4px;
    text-align: center;
    z-index: 2;
  }
  .proposal-content {
    padding: 0 30px;
    li {
      height: 200px;
      .proposal-content-lf {
        width: 72%;
        display: inline-block;
        h4 {
          font-size: 16px;
          color: #444444;
          margin: 10px 0;
        }
        p {
          font-size: 14px;
          color: #666666;
          text-align: justify;
          width: 100%;
          height: 144px;
          line-height: 24px;
          word-break: break-word;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 6;
        }
      }
      .proposal-content-rt {
        width: 20%;
        display: inline-block;
        margin-left: 61px;
        float: right;
        padding-top: 95px;
        .el-progress,
        .el-progress-bar {
          width: 130px;
          height: 20px;
        }
        .el-progress-bar__inner {
          background: #4f81f4;
        }
        p {
          font-size: 14px;
          color: #444444;
          margin-top: 18px;
          padding-right: 40px;
          text-align: center;
        }
      }
    }
  }
  .noTask-container {
    margin: 0 auto;
    padding-bottom: 50px;
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
  }
}
</style>
