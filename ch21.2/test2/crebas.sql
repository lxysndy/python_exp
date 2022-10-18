/*==============================================================*/
/* 股票信息数据库DDL脚本                                        */
/* 代码文件：代码\chapter22\22.4\db\crebas.sql                  */
/*==============================================================*/

/* 创建数据库 */
create database ch21;

use ch21;

drop table if exists excel;
/*5.9号的股票*/
/*==============================================================*/
/* Table: HistoricalQuote                                       */
/*==============================================================*/
create table excel
(
   Name                 varchar(20),
   Open                 float,
   Close                float,
   RiseAndUp            float,
   RiseAndUpA           varchar(20),
   High                 float,
   Low                  float,
   Volume               bigint,
   Money                float,
   TurnoverRate         varchar(20)
);


select * from excel