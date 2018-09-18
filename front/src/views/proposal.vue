<template>
  <div class="proposal-index-container">
    <div class="header-wrap">
      <top-Header></top-Header>
    </div>
    <div class="container">
      <div class="create-wrap" @click="goApply">
        <span style="cursor: pointer">
            <i class="el-icon-plus"></i>
          <span>创建提案</span>
        </span>
      </div>

      <el-tabs v-model="proposalIndexTabs" @tab-click="handleClick" class="proposal-tabs-wrap">
        <!-- 投票中的提案 -->

        <el-tab-pane label="投票中的提案" name="first">
          <div v-if="!loading">
            <ul class="voting-list" v-if="proposalList.length !== 0">

              <li v-for="item in proposalList" :key="item.index">
                <h4 @click="goDetail(item.proposalId, item.displayName, item.periodStatus)">{{item.proposalName}}</h4>
                <p class="avatar-wrap">
                  <img :src="item.avator" alt="">
                  <span>{{item.displayName}}</span>
                </p>
                <div class="content-wrap">
                  <p class="content-lf">{{item.digest}}</p>
                  <div class="content-rt">
                    <p>每期{{ item.balance }}UT，第{{item.periodCurrentNo}}期</p>
                    <p class="progress-color-blue">
                      <el-progress :text-inside="true" :percentage="item.voteNumYes | progress(data.majorNodeCount)" status="success"></el-progress>
                    </p>
                    <p class="vote-state">投票：{{item.voteNumYes}}票
                      <span v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">（投票统计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">（未通过）</span>
                      <span v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">（投票计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">（未通过）</span>
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </el-tab-pane>

        <!-- 所有提案 -->
        <el-tab-pane label="所有提案" name="second">
          <div v-if="!loading">
            <ul class="voting-list" v-if="proposalList.length !== 0">
              <li v-for="item in proposalList" :key="item.index">
                <h4 @click="goDetail(item.proposalId, item.displayName, item.periodStatus)">{{item.proposalName}}</h4>
                <p class="avatar-wrap">
                  <img :src="item.avator" alt="">
                  <span>{{item.displayName}}</span>
                </p>
                <div class="content-wrap">
                  <div class="content-lf">
                    {{item.digest}}
                  </div>
                  <div class="content-rt">
                    <p>每期{{ item.balance }}UT，第{{item.periodCurrentNo}}期</p>
                    <p class="progress-color-red">
                      <el-progress :text-inside="true" :percentage="item.voteNumYes | progress(data.majorNodeCount)" status="success" v-if="item.periodStatus == 0"></el-progress>
                      <el-progress :text-inside="true" :percentage="item.voteNumYes | progress(data.majorNodeCount)" v-else-if="item.periodStatus == 1"></el-progress>
                      <el-progress :text-inside="true" :percentage="item.voteNumYes | progress(data.majorNodeCount)" status="exception" v-else-if="item.periodStatus == 2"></el-progress>
                    </p>
                    <p class="vote-state">
                      投票：{{item.voteNumYes}}票
                      <span v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">（投票统计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">（未通过）</span>
                      <span v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">（投票计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">（未通过）</span>
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </el-tab-pane>

        <el-tab-pane label="已通过的提案" name="third">
          <div v-if="!loading">
            <ul class="voting-list" v-if="proposalList.length !== 0">
              <div class="create-wrap">
              </div>
              <li v-for="item in proposalList" :key="item.index">
                <h4 @click="goDetail(item.proposalId, item.displayName, item.periodStatus)">{{item.proposalName}}</h4>
                <p class="avatar-wrap">
                  <img :src="item.avator" alt="">
                  <span>{{item.displayName}}</span>
                </p>
                <div class="content-wrap">
                  <div class="content-lf">
                    <p class="details">
                      支付次数：
                      <span>{{item.periodCurrentNo}}次</span>
                    </p>
                    <p class="details">
                      支付总额：
                      <span>{{item.payBalance}} UT</span>
                    </p>
                    <p class="details">
                      结束时间：
                      <span>{{data.voteTimeEnd | timeDate}}</span>
                    </p>
                  </div>
                  <div class="content-rt">
                    <p>当期{{item.balance}}UT，第{{item.periodCurrentNo}}期</p>
                    <p class="state-type1">
                      <el-progress :text-inside="true" :percentage="item.voteNumYes | progress(data.majorNodeCount)"></el-progress>
                    </p>
                    <p class="vote-state">
                      投票结束：{{item.voteNumYes}}票
                      <span v-if="item.periodStatus==0 && data.isVoteTimeEnd == true">（投票统计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == true">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == true">（未通过）</span>
                      <span v-else-if="item.periodStatus==0 && data.isVoteTimeEnd == false">（投票计中）</span>
                      <span v-else-if="item.periodStatus==1 && data.isVoteTimeEnd == false">（已通过）</span>
                      <span v-else-if="item.periodStatus==2 && data.isVoteTimeEnd == false">（未通过）</span>
                    </p>
                  </div>
                </div>
              </li>

            </ul>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
  import {
    getAllProposal
  } from "@/api/api";
  import store from "../store";
  import {
    apiUrl
  } from "@/api/url";
  export default {
    data() {
      return {
        data: null,
        value: "",
        proposalIndexTabs: "first",
        proposalList: [],
        loading: true,
        per: 0,
        apiU: apiUrl
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
          return "（投票中）";
        } else if (value == 1) {
          return "（已通过）";
        } else if (value == 2) {
          return "（未通过）";
        }
      }
    },
    methods: {
      goDetail(id, name, status) {
        this.$router.push({
          path: "/proposalDetail",
          query: {
            id: id,
            name: name,
            status: status
          }
        });
      },

      goApply() {
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
            path: "/proposalApply"
          });
        }
      },
      handleClick(tab, event) {
        if (tab.index == 0) {
          this.getList(1, 100, 1);
        } else if (tab.index == 1) {
          this.getList(0, 100, 1);
        } else {
          this.getList(tab.index, 100, 1);
        }
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
        getAllProposal(searchType, pageSize, pageNumber).then(res => {
          this.data = res;
          this.proposalList = res.proposalDoList;
          loading.close();
          this.loading = false;
        });
      }
    },
    mounted() {
      this.getList(1, 100, 1);
    }
  };
</script>

<style rel="stylesheet/scss" lang="scss">
  .proposal-index-container {
    // tabs start
    .proposal-tabs-wrap .el-tabs__nav {
      margin: 58px auto 68px;
    }
    .proposal-tabs-wrap .el-tabs__active-bar,
    .el-tabs__nav-wrap::after {
      display: none;
    }
    .proposal-tabs-wrap .el-tabs__item {
      font-size: 14px;
      color: #999999;
    }
    .proposal-tabs-wrap .el-tabs__item.is-active {
      font-size: 16px;
      color: #333333;
    }
    // tabs end
    // 进度条
    .el-progress.is-success .el-progress-bar__inner {
      height: 6px;
      background-color: #4F81F4;
    }
    .el-progress-bar {
      height: 4px;
    }
    .el-progress {
      height: 6px;
    }
    .el-progress-bar__outer {
      height: 4px;
      background-color: #eee;
    }
    .progress-color-blue {
      height: 4px;
      .el-progress-bar__inner {
        border-radius: 47px;
      }
    }
    .progress-color-green {
      height: 6px;
      .el-progress-bar__inner {
        border-radius: 47px;
      }
    }
    .progress-color-red {
      height: 6px;
      .el-progress-bar__inner {
        border-radius: 47px;
      }
    }
  }
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  .proposal-index-container {
    height: 100%;
    background-color: #fff;
    padding-top: 55px;
    padding-bottom: 291px;
    .container {
      width: 1200px;
      margin: 0 auto;
    }
    // 投票中的提案
    .voting-list {
      width: 100%;
      clear: both;
      li {
        width: 100%;
        height: 290px;
        border-bottom: 1px solid #dedede;
        box-sizing: border-box;
        h4 {
          font-size: 24px;
          color: #282828;
          line-height: 40px;
          margin: 30px 0 23px;
          cursor: pointer;
          display: inline-block;
        }
        .avatar-wrap {
          img {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #282828;
            vertical-align: bottom;
          }
          span {
            font-size: 14px;
            color: #999999;
            margin-left: 10px;
            display: inline-block;
            vertical-align: top;
          }
        }
        .content-wrap {
          .content-lf {
            width: 71%;
            height: 96px;
            font-size: 14px;
            color: #282828;
            text-align: justify;
            line-height: 24px;
            padding: 23px 38px 0 0;
            float: left;
            margin-bottom: 55px;
            font-size: 14px;
            word-break: break-word;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            .details {
              font-size: 16px;
              color: #666666;
              width: 241px;
              display: inline-block;
              padding-top: 35px;
              span {
                font-size: 16px;
                color: #333333;
                margin-left: 10px;
              }
            }
          }
          .content-rt {
            width: 22%;
            padding-left: 42px;
            display: inline-block;
            border-left: 1px solid #dedede;
            p {
              margin-bottom: 24px;
              &:first-child {
                font-size: 14px;
                color: #333333;
              }
            }
            .vote-state {
              font-size: 14px;
              color: #409ced;
              span {
                font-size: 14px;
                color: #999;
                line-height: 21px;
              }
            }
          }
        }
      }
    }
    // 创建提案
    .create-wrap {
      position: absolute;
      right: 0;
      top: 48px;
      z-index: 2;
      i {
        display: inline-block;
        font-size: 16px;
        color: #4f81f4;
        font-weight: bold;
      }
      span {
        font-size: 16px;
        color: #4f81f4;
      }
    }
  }
</style>

