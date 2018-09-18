<template>
  <div class="proposalDetails-container">
      <div class="header-wrap">
      <top-Header></top-Header>
      </div>
    <div class="container" v-if="!loading">
         <div class="topTitle-wrap">
            <router-link to="/personal/myProposal" class="topTitle-back">返回提案管理</router-link>
         </div>
         <div class="basic-information-wrap">
            <h4>基本信息</h4>
            <ul class="info-list">
              <li>
                <span class="name">注册主节点</span>
                <span class="content">{{data.majorNodeCount}}</span>
              </li>
               <li>
                <span class="name">投票截止时间</span>
                <span class="content">{{data.voteTimeEnd | timeDate}}</span>
              </li>
               <li>
                <span class="name">区块高度</span>
                <span class="content">{{data.superBlockHeight}}</span>
              </li>
            </ul>
         </div>
         <div class="table-wrap">
            <table>
                <tbody>
                  <tr>
                    <td class="table-name">标题</td>
                    <td class="table-content">{{data.proposalDetailDo.proposalName}}</td>
                  </tr>
                  <tr>
                    <td class="table-name">所有者</td>
                    <td class="table-content">{{name}}</td>
                  </tr>
                  <tr>
                    <td class="table-name">付款</td>
                    <td v-if="data.proposalDetailDo.payBalance == 0" class="table-content">尚未付款（共{{data.proposalDetailDo.periodCount}}期）</td>
                    <td v-else class="table-content">第{{data.proposalDetailDo.periodCurrentNo}}期（共{{data.proposalDetailDo.periodCount}}个期）</td>
                  </tr>
                  <tr>
                    <td class="table-name">投票</td>
                    <td class="table-content vote">
                        <span>是：{{data.proposalDetailDo.voteNumYes}}</span>
                        <span>否：{{data.proposalDetailDo.voteNumNo}}</span>
                        <span>弃权：{{data.proposalDetailDo.voteNumAbstain}}</span>
                    </td>
                  </tr>
                  <!-- <tr>
                    <td class="table-name">是否会被资助</td>
                    <td class="table-content">
                      否&nbsp;&nbsp;&nbsp;&nbsp;此提案还需要额外XX票才能进入UT简历预选名单。（总节点数的20%）
                    </td>
                  </tr> -->
                  <tr>
                    <td class="table-name">提案附件</td>
                    <td class="table-content">
                        <a :href="data.proposalDetailDo.attachmentFile" download="a.zip">下载</a>
                    </td>
                  </tr>
                  <tr>
                    <td class="table-name">提案附加链接</td>
                    <td class="table-content">
                      <a  target="_blank" :href="data.proposalDetailDo.additionalLink">{{data.proposalDetailDo.additionalLink}}</a>
                    </td>
                  </tr>
                </tbody>
            </table>
         </div>
         <div class="proposal-details-wrap">
            <h4>提案详情</h4>
            <p>
              {{data.proposalDetailDo.content}}
            </p>
         </div>
         <div class="vote-wrap" >
           <h4>投票</h4>
           <div class="vote-content-wrap" v-if="status== 0 && data.isVoteTimeEnd == false">
             <div class="vote-lf-wrap">
                 <el-radio-group v-model="voteRadio" class="voteRadio-wrap">
                    <el-radio :label="0">是</el-radio>
                    <el-radio :label="1">否</el-radio>
                    <el-radio :label="2">弃权</el-radio>
                </el-radio-group>
             </div>
             <div class="vote-rt-wrap">
                <el-button type="primary" @click="onSubmit(data.proposalDetailDo.proposalPeriodId,data.proposalDetailDo.proposalId, voteRadio)" class="submit-btn" :disabled="!canVote">确认投票</el-button>
             </div>

           </div>
           <div class="end"  v-else>投票已结束</div>
         </div>
    </div>

  </div>
</template>
<script>
import { getProposalDetail, vote } from "@/api/api";
import { apiUrl } from "@/api/url";
export default {
  data() {
    return {
      voteRadio: "3",
      nowTime: new Date(),
      data: null,
      name: this.$route.query.name,
      fileUrl: apiUrl,
      loading: true,
      status: this.$route.query.status,
      canVote:true
    };
  },
  methods: {

    onSubmit(id, proposalId, voteRadio) {
      this.canVote = false
      setTimeout(()=>{
        this.canVote = true
      },3000)
      if (voteRadio == '3') {
        this.$notify({
          title: "失败",
          message: "请选择您要投的票",
          type: "error"
        });
        return;
      }
      vote(id,proposalId,  voteRadio).then(res => {
        if (res.success) {
          this.$notify({
            title: "成功",
            message: "投票成功",
            type: "success"
          });
          this.getDetail(this.$route.query.id);
        } else {
          if (res.errorCode == "100022") {
            this.$notify({
              message: "您还不是主节点，暂时不能投票",
              type: "warning"
            });
          }
        }
      });
    },
    getDetail(id) {
      this.loading = true;
      getProposalDetail(id).then(res => {
        if (res.success) {
          this.data = res;
          this.loading = false;
        }
      });
    }
  },
  mounted() {
    this.getDetail(this.$route.query.id);
  }

};
</script>
<style rel="stylesheet/scss" lang="scss">
.proposalDetails-container{
   // 单选按钮 start
  .voteRadio-wrap{
     font-size: 18px;
      color: #444444;
    .el-radio {
      font-size: 18px;
      color: #444444;
      margin-right: 76px;
    }
    .el-radio__inner {
      width: 28px;
      height: 28px;
      background: #ffffff;
      border: 1px solid #979797;
    }
    .el-radio__input.is-checked .el-radio__inner {
      background: transparent;
      border-color: #979797;
    }
    .el-radio__inner::after {
      width: 16px;
      height: 16px;
      background: #4f81f4;
    }
  }
  // 单选按钮 end
}
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.proposalDetails-container {
  background-color: #f4f4f4;
  padding-top: 75px;
  .container {
    width: 1200px;
    margin: 0 auto;
    background-color: #ffffff;
    padding-bottom: 125px;
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

    .end {
      font-size: 14px;
    color: #666666;
    text-align: justify;
    line-height: 24px;
    margin: 0 110px 30px 112px;
    }

  .basic-information-wrap {
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 30px 0 26px 92px;
    }
    .info-list {
      li {
        margin-left: 112px;
        margin-bottom: 21px;
        &::before {
          content: "";
          display: inline-block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #d8d8d8;
          vertical-align: middle;
          margin-right: 10px;
        }
        .name {
          font-size: 14px;
          color: #666666;
          width: 120px;
          display: inline-block;
        }
        .content {
          font-size: 14px;
          color: #666666;
        }
      }
    }
  }
  .table-wrap {
    border-bottom: 1px solid #eee;
    table {
      margin: 40px 48px 40px 52px;
      border-collapse: collapse;
    }
    td {
      background: #ffffff;
      border: 1px solid #ebebeb;
      box-sizing: border-box;
      vertical-align: middle;
      overflow: hidden;
      line-height: 24px;
    }
    .table-name {
      width: 240px;
      height: 60px;
      padding-left: 60px;
      font-size: 16px;
      color: #444444;
    }
    .table-content {
      width: 861px;
      height: 60px;
      padding: 15px 61px;
      font-size: 14px;
      color: #666666;
      word-break: break-word;
      text-align: justify;
    }
    .table-link {
      font-size: 14px;
      color: #2a70da;
    }
    .vote span {
      width: 126px;
      display: inline-block;
    }
  }
  .proposal-details-wrap {
    border-bottom: 1px solid #eee;
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 30px 0 26px 92px;
    }
    p {
      font-size: 14px;
      color: #666666;
      text-align: justify;
      line-height: 24px;
      margin: 0 110px 30px 112px;
    }
  }
  .vote-wrap {
    border-bottom: 1px solid #eee;
    h4 {
      font-size: 18px;
      color: #444444;
      margin: 30px 0 26px 92px;
    }
    .vote-content-wrap {
      margin: 0 0 52px 114px;
    }
    .vote-lf-wrap {
      display: inline-block;
    }
    .vote-rt-wrap {
      display: inline-block;
      // 提交按钮 start
      .submit-btn {
        background: #4f81f4;
        width: 100px;
        height: 44px;
        line-height: 44px;
        padding: 0;
        font-size: 14px;
        color: #ffffff;
      }
      .submit-btn[disabled]{
        background:gray!important;
        border-color:gray!important;
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
        border: none;
      }
      // 提交按钮 end
    }

  }
}
</style>

