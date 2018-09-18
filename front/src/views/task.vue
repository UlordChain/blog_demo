<template>
  <div class="bountyMissions-container">
    <div class="header-wrap">
      <top-Header></top-Header>
  </div>
    <div class="container">
      <!-- 申请任务 start -->
      <div class="bountyMissions">
         <div class="topTitle-wrap">
           <h4>Ulord跨链集成</h4>
           <p>
             赏金<span>200UT</span>
            </p>
         </div>
         <div class="table-wrap">
            <table>
                <tbody>
                  <tr>
                    <td class="table-name">任务描述</td>
                    <td class="table-content">使Ulord支持与bitcoin,zcash,dash.decrwd,Litecoin等币中跨链交易</td>
                  </tr>
                  <tr>
                    <td class="table-name">开发周期</td>
                    <td class="table-content">不超过60天</td>
                  </tr>
                  <tr>
                    <td class="table-name">开发工作量</td>
                    <td class="table-content">2人月</td>
                  </tr>
                  <tr>
                    <td class="table-name">开发语言</td>
                    <td class="table-content">Go</td>
                  </tr>
                  <tr class="large-box">
                    <td class="table-name">参考文献</td>
                    <td class="table-content">
                       <ul class="explain-list">
                        <li>
                          <span>官方支持</span>
                          <router-link to="https://github.com/UlordChain/ulord-blog-demo" class="table-link">
                            https://github.com/UlordChain/ulord-blog-demo
                          </router-link>
                        </li>
                        <li>
                          <span>开发文档</span>
                          <router-link to="https://github.com/UlordChain/ulord-blog-demo" class="table-link">
                            开发环境
                          </router-link>
                        </li>
                      </ul>
                    </td>
                  </tr>
                  <tr class="large-box">
                    <td class="table-name">需求说明</td>
                    <td class="table-content ">
                      <ul class="explain-list">
                        <li>个人档案记录每个人的信誉度（由回答次数、履约次数等组成）作为参考</li>
                        <li>平台中的每笔交易要在链上可查、公开透明，并在页面中标明对应的交易</li>
                        <li>编写详细的部署文档和开发教程</li>
                        <li>进度在github上更新</li>
                      </ul>
                    </td>
                  </tr>
                </tbody>
            </table>
            <div class="submit-btn-wrap">
                 <el-button type="primary" class="submit-btn">申请任务</el-button>
            </div>

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
export default {
  data() {
    return {
    }
  },
  methods: {

  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
body{
  background-color: #FFFFFF;
}
.bountyMissions-container{
   padding-bottom: 125px;
    .container{
      width: 1200px;
      margin: 0 auto;
    }
  /*====================================
           赏金任务申请
  =====================================*/
    .bountyMissions{
      display: none;
    }
    .topTitle-wrap{
      margin-top: 40px;
      position: relative;
      height: 126px;
      color: #FFFFFF;
      text-align: center;
      background: #4F81F4;
      h4{
        font-size: 24px;
        padding: 22px 0 15px;
      }
      p{
        font-size: 24px;
        line-height: 36px;
        span{
          font-weight: bold;
          margin-left: 20px;
        }

      }
    }
    // 表格布局 start
    .table-wrap{
      table{
        margin: 40px 48px 40px 52px;
        border-collapse:collapse;
      }
      td{
        background: #FFFFFF;
        border: 1px solid #EBEBEB;
        box-sizing: border-box;
        p{
          font-size: 14px;
          color: #666666;
          text-align: justify;
          line-height: 24px;
        }
      }
      .table-name{
        width: 240px;
        height: 60px;
        padding-left: 60px;
        font-size: 16px;
        color: #444444;
      }
      .table-content{
        width: 861px;
        height: 60px;
        padding: 0 61px;
        font-size: 14px;
        color: #666666;
        .explain-list{
          li{
            margin-bottom: 14px;
            &::before{
              content: '';
              width: 8px;
              height: 8px;
              border-radius: 50%;
              background: #D8D8D8;
              display: inline-block;
              margin-right: 10px;
            }
            &:last-child{
              margin-bottom: 0;
            }
            span{
              font-size: 14px;
              color: #666666;
              margin-right: 20px;
            }
          }
        }
        .word-count{
          font-size: 14px;
          color: #666666;
          text-align: right;
          line-height: 24px;
          .used{
            color: #3F3F3F;
          }
          .total{
            font-size: 14px;
            color: #666666;
          }
        }
      }
      .table-link{
        font-size: 14px;
        color: #4F81F4;
      }
      .large-box td{
        vertical-align: top;
        padding-top: 20px;
        padding-bottom: 20px;
      }
    }
     // 表格布局 end
     // 提交按钮 start
    .submit-btn-wrap{
        margin: 0 auto;
        text-align: center;
     }
    .submit-btn{
        background: #4F81F4;
        width: 320px;
        height: 60px;
        line-height: 60px;
        padding: 0;
        font-size: 18px;
        color: #FFFFFF;
    }
    .el-button--primary:focus, .el-button--primary:hover {
        background: #4F81F4;
        width: 320px;
        height: 60px;
        line-height: 60px;
        padding: 0;
        font-size: 18px;
        color: #FFFFFF;
    }
    /*====================================
           申请反馈
    =====================================*/
    .bountyMissions-state{
      margin: 40px auto;
      height: 480px;
      background: #FFFFFF;
      box-shadow: 0 2px 4px 0 rgba(210,210,210,0.50);
      border-radius: 4px;
      text-align: center;
      h4{
        font-size: 20px;
        color: #444444;
        padding-top: 112px;
        i{
          font-size: 24px;
          display: inline-block;
          color: #6BC00C;
          vertical-align: text-bottom;
        }
      }
      p{
        font-size: 16px;
        color: #666666;
        margin: 28px 0 50px;
      }
      .backHome{
        font-size: 14px;
        color: #D37015;
      }
    }
  }

</style>

