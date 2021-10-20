module Chain (
  input logic [1:0] accessor_output,
  input logic [1:0] [15:0] chain_data_in,
  input logic chain_en,
  input logic clk_en,
  input logic [1:0] [15:0] curr_tile_data_out,
  input logic flush,
  output logic [1:0] [15:0] data_out_tile
);

always_comb begin
  if (accessor_output[0]) begin
    data_out_tile[0] = curr_tile_data_out[0];
  end
  else if (chain_en) begin
    data_out_tile[0] = chain_data_in[0];
  end
  else data_out_tile[0] = 16'h0;
  if (accessor_output[1]) begin
    data_out_tile[1] = curr_tile_data_out[1];
  end
  else if (chain_en) begin
    data_out_tile[1] = chain_data_in[1];
  end
  else data_out_tile[1] = 16'h0;
end
endmodule   // Chain

module LakeTop (
  input logic [1:0] accessor_output_top,
  input logic [1:0] [15:0] addr_in,
  input logic [8:0] addr_to_sram_top,
  input logic cen_to_sram_top,
  input logic chain_chain_en,
  input logic [1:0] [15:0] chain_data_in,
  input logic clk,
  input logic clk_en,
  input logic [7:0] config_addr_in,
  input logic [31:0] config_data_in,
  input logic [1:0] config_en,
  input logic config_read,
  input logic config_write,
  input logic [1:0] [15:0] data_in,
  input logic [1:0] [15:0] data_out_top,
  input logic [3:0] [15:0] data_to_sram_top,
  input logic [15:0] fifo_ctrl_fifo_depth,
  input logic flush,
  input logic [1:0] [2:0] loops_sram2tb_mux_sel_top,
  input logic [1:0] loops_sram2tb_restart_top,
  input logic [1:0] mode,
  input logic [1:0] ren_in,
  input logic rst_n,
  input logic [3:0] strg_ub_agg_only_agg_read_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] strg_ub_agg_only_agg_read_addr_gen_0_strides,
  input logic [3:0] strg_ub_agg_only_agg_read_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] strg_ub_agg_only_agg_read_addr_gen_1_strides,
  input logic [3:0] strg_ub_agg_only_agg_write_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] strg_ub_agg_only_agg_write_addr_gen_0_strides,
  input logic [3:0] strg_ub_agg_only_agg_write_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] strg_ub_agg_only_agg_write_addr_gen_1_strides,
  input logic strg_ub_agg_only_agg_write_sched_gen_0_enable,
  input logic [15:0] strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_strides,
  input logic strg_ub_agg_only_agg_write_sched_gen_1_enable,
  input logic [15:0] strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_strides,
  input logic [3:0] strg_ub_agg_only_loops_in2buf_0_dimensionality,
  input logic [5:0] [15:0] strg_ub_agg_only_loops_in2buf_0_ranges,
  input logic [3:0] strg_ub_agg_only_loops_in2buf_1_dimensionality,
  input logic [5:0] [15:0] strg_ub_agg_only_loops_in2buf_1_ranges,
  input logic strg_ub_agg_sram_shared_agg_read_sched_gen_0_enable,
  input logic [15:0] strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides,
  input logic strg_ub_agg_sram_shared_agg_read_sched_gen_1_enable,
  input logic [15:0] strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides,
  input logic [3:0] strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality,
  input logic [5:0] [15:0] strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_ranges,
  input logic [3:0] strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality,
  input logic [5:0] [15:0] strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_ranges,
  input logic [1:0] t_read_out_top,
  input logic tile_en,
  input logic [1:0] wen_in,
  input logic wen_to_sram_top,
  output logic [1:0] [31:0] config_data_out,
  output logic [1:0] [15:0] data_out,
  output logic empty,
  output logic [1:0][3:0] [15:0] formal_agg_data_out,
  output logic full,
  output logic sram_ready_out,
  output logic [1:0] valid_out
);

logic [1:0] accessor_output;
logic [2:0][0:0][8:0] all_addr_to_mem;
logic [2:0][15:0] all_data_out;
logic [2:0][0:0][3:0][15:0] all_data_to_mem;
logic [2:0][0:0] all_ren_to_mem;
logic [2:0] all_valid_out;
logic [2:0][0:0] all_wen_to_mem;
logic cfg_seq_clk;
logic [1:0] chain_accessor_output;
logic [15:0] config_data_in_shrt;
logic [1:0][15:0] config_data_out_shrt;
logic config_seq_clk;
logic config_seq_clk_en;
logic [15:0] cycle_count;
logic [1:0][15:0] data_out_tile;
logic [0:0][8:0] fifo_addr_to_mem;
logic fifo_ctrl_clk;
logic [15:0] fifo_ctrl_data_in;
logic fifo_ctrl_pop;
logic fifo_ctrl_push;
logic [15:0] fifo_data_out;
logic [0:0][3:0][15:0] fifo_data_to_mem;
logic fifo_empty;
logic fifo_full;
logic fifo_ren_to_mem;
logic fifo_valid_out;
logic fifo_wen_to_mem;
logic gclk;
logic [8:0] mem_addr_cfg;
logic [0:0][0:0][8:0] mem_addr_dp;
logic [0:0][0:0][8:0] mem_addr_in;
logic [0:0] mem_cen_dp;
logic [0:0] mem_cen_in;
logic [3:0][15:0] mem_data_cfg;
logic [0:0][0:0][3:0][15:0] mem_data_dp;
logic [0:0][0:0][3:0][15:0] mem_data_in;
logic [0:0][3:0][15:0] mem_data_low_pt;
logic [0:0][0:0][3:0][15:0] mem_data_out;
logic mem_ren_cfg;
logic mem_wen_cfg;
logic [0:0] mem_wen_dp;
logic [0:0] mem_wen_in;
logic [1:0] mode_mask;
logic [0:0][8:0] sram_addr_to_mem;
logic sram_ctrl_clk;
logic [15:0] sram_ctrl_data_in;
logic [15:0] sram_ctrl_rd_addr_in;
logic sram_ctrl_ren;
logic sram_ctrl_wen;
logic [15:0] sram_ctrl_wr_addr_in;
logic [15:0] sram_data_out;
logic [0:0][3:0][15:0] sram_data_to_mem;
logic sram_ren_to_mem;
logic sram_valid_out;
logic sram_wen_to_mem;
logic [1:0] strg_ub_accessor_output_top;
logic [8:0] strg_ub_addr_to_sram_top;
logic strg_ub_cen_to_sram_top;
logic strg_ub_clk;
logic [1:0][15:0] strg_ub_data_out_top;
logic [3:0][15:0] strg_ub_data_to_sram_top;
logic [1:0][2:0] strg_ub_loops_sram2tb_mux_sel_top;
logic [1:0] strg_ub_loops_sram2tb_restart_top;
logic [1:0] strg_ub_t_read_out_top;
logic strg_ub_wen_to_sram_top;
logic [0:0][0:0][8:0] ub_addr_to_mem;
logic [0:0] ub_cen_to_mem;
logic [1:0][15:0] ub_data_out;
logic [0:0][0:0][3:0][15:0] ub_data_to_mem;
logic [1:0] ub_valid_out;
logic [0:0] ub_wen_to_mem;
assign config_data_in_shrt = config_data_in[15:0];

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    cycle_count <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      cycle_count <= 16'h0;
    end
    else cycle_count <= cycle_count + 16'h1;
  end
end
assign config_data_out[0] = 32'(config_data_out_shrt[0]);
assign config_data_out[1] = 32'(config_data_out_shrt[1]);
assign gclk = clk & tile_en;
assign mem_data_low_pt[0] = mem_data_out[0][0];
assign cfg_seq_clk = gclk;
assign config_seq_clk = cfg_seq_clk;
assign config_seq_clk_en = clk_en | (|config_en);
assign mem_wen_in = (|config_en) ? mem_wen_cfg: mem_wen_dp;
assign mem_cen_in = (|config_en) ? mem_wen_cfg | mem_ren_cfg: mem_cen_dp;
assign mem_addr_in[0][0] = (|config_en) ? mem_addr_cfg: mem_addr_dp[0][0];
assign mem_data_in[0][0] = (|config_en) ? mem_data_cfg: mem_data_dp[0][0];
assign strg_ub_clk = gclk;
assign sram_ctrl_clk = gclk;
assign sram_ctrl_wen = wen_in[0];
assign sram_ctrl_ren = ren_in[0];
assign sram_ctrl_data_in = data_in[0];
assign sram_ctrl_wr_addr_in = addr_in[0];
assign sram_ctrl_rd_addr_in = addr_in[0];
assign fifo_ctrl_clk = gclk;
assign fifo_ctrl_data_in = data_in[0];
assign fifo_ctrl_push = wen_in[0];
assign fifo_ctrl_pop = ren_in[0];
assign empty = fifo_empty;
assign full = fifo_full;
assign all_data_to_mem[0] = ub_data_to_mem;
assign all_wen_to_mem[0] = ub_wen_to_mem;
assign all_ren_to_mem[0] = ub_cen_to_mem;
assign all_addr_to_mem[0] = ub_addr_to_mem;
assign all_data_to_mem[1] = fifo_data_to_mem;
assign all_wen_to_mem[1] = fifo_wen_to_mem;
assign all_ren_to_mem[1] = fifo_ren_to_mem;
assign all_addr_to_mem[1][0] = fifo_addr_to_mem[0];
assign all_data_to_mem[2] = sram_data_to_mem;
assign all_wen_to_mem[2] = sram_wen_to_mem;
assign all_ren_to_mem[2] = sram_ren_to_mem;
assign all_addr_to_mem[2][0] = sram_addr_to_mem[0];
assign mem_data_dp = all_data_to_mem[mode];
assign mem_cen_dp = all_ren_to_mem[mode] | all_wen_to_mem[mode];
assign mem_wen_dp = all_wen_to_mem[mode];
assign mem_addr_dp = all_addr_to_mem[mode];
assign all_data_out[0] = ub_data_out[0];
assign all_valid_out[0] = ub_valid_out[0];
assign all_data_out[1] = fifo_data_out;
assign all_valid_out[1] = fifo_valid_out;
assign all_data_out[2] = sram_data_out;
assign all_valid_out[2] = sram_valid_out;
assign data_out_tile[0] = all_data_out[mode];
assign valid_out[0] = all_valid_out[mode];
assign data_out_tile[1] = ub_data_out[1];
assign valid_out[1] = ub_valid_out[1];
assign mode_mask[0] = |mode;
assign mode_mask[1] = 1'h0;
assign chain_accessor_output = accessor_output | mode_mask;
assign strg_ub_cen_to_sram_top = cen_to_sram_top;
assign strg_ub_data_to_sram_top = data_to_sram_top;
assign strg_ub_wen_to_sram_top = wen_to_sram_top;
assign strg_ub_addr_to_sram_top = addr_to_sram_top;
assign strg_ub_loops_sram2tb_mux_sel_top = loops_sram2tb_mux_sel_top;
assign strg_ub_loops_sram2tb_restart_top = loops_sram2tb_restart_top;
assign strg_ub_t_read_out_top = t_read_out_top;
assign strg_ub_accessor_output_top = accessor_output_top;
assign strg_ub_data_out_top = data_out_top;
storage_config_seq config_seq (
  .clk(config_seq_clk),
  .clk_en(config_seq_clk_en),
  .config_addr_in(config_addr_in),
  .config_data_in(config_data_in_shrt),
  .config_en(config_en),
  .config_rd(config_read),
  .config_wr(config_write),
  .flush(flush),
  .rd_data_stg(mem_data_low_pt),
  .rst_n(rst_n),
  .addr_out(mem_addr_cfg),
  .rd_data_out(config_data_out_shrt),
  .ren_out(mem_ren_cfg),
  .wen_out(mem_wen_cfg),
  .wr_data(mem_data_cfg)
);

strg_ub_vec strg_ub (
  .accessor_output_top(strg_ub_accessor_output_top),
  .addr_to_sram_top(strg_ub_addr_to_sram_top),
  .agg_only_agg_read_addr_gen_0_starting_addr(strg_ub_agg_only_agg_read_addr_gen_0_starting_addr),
  .agg_only_agg_read_addr_gen_0_strides(strg_ub_agg_only_agg_read_addr_gen_0_strides),
  .agg_only_agg_read_addr_gen_1_starting_addr(strg_ub_agg_only_agg_read_addr_gen_1_starting_addr),
  .agg_only_agg_read_addr_gen_1_strides(strg_ub_agg_only_agg_read_addr_gen_1_strides),
  .agg_only_agg_write_addr_gen_0_starting_addr(strg_ub_agg_only_agg_write_addr_gen_0_starting_addr),
  .agg_only_agg_write_addr_gen_0_strides(strg_ub_agg_only_agg_write_addr_gen_0_strides),
  .agg_only_agg_write_addr_gen_1_starting_addr(strg_ub_agg_only_agg_write_addr_gen_1_starting_addr),
  .agg_only_agg_write_addr_gen_1_strides(strg_ub_agg_only_agg_write_addr_gen_1_strides),
  .agg_only_agg_write_sched_gen_0_enable(strg_ub_agg_only_agg_write_sched_gen_0_enable),
  .agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr(strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr),
  .agg_only_agg_write_sched_gen_0_sched_addr_gen_strides(strg_ub_agg_only_agg_write_sched_gen_0_sched_addr_gen_strides),
  .agg_only_agg_write_sched_gen_1_enable(strg_ub_agg_only_agg_write_sched_gen_1_enable),
  .agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr(strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr),
  .agg_only_agg_write_sched_gen_1_sched_addr_gen_strides(strg_ub_agg_only_agg_write_sched_gen_1_sched_addr_gen_strides),
  .agg_only_loops_in2buf_0_dimensionality(strg_ub_agg_only_loops_in2buf_0_dimensionality),
  .agg_only_loops_in2buf_0_ranges(strg_ub_agg_only_loops_in2buf_0_ranges),
  .agg_only_loops_in2buf_1_dimensionality(strg_ub_agg_only_loops_in2buf_1_dimensionality),
  .agg_only_loops_in2buf_1_ranges(strg_ub_agg_only_loops_in2buf_1_ranges),
  .agg_sram_shared_agg_read_sched_gen_0_enable(strg_ub_agg_sram_shared_agg_read_sched_gen_0_enable),
  .agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr(strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr),
  .agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides(strg_ub_agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides),
  .agg_sram_shared_agg_read_sched_gen_1_enable(strg_ub_agg_sram_shared_agg_read_sched_gen_1_enable),
  .agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr(strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr),
  .agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides(strg_ub_agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides),
  .agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality(strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality),
  .agg_sram_shared_loops_in2buf_autovec_write_0_ranges(strg_ub_agg_sram_shared_loops_in2buf_autovec_write_0_ranges),
  .agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality(strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality),
  .agg_sram_shared_loops_in2buf_autovec_write_1_ranges(strg_ub_agg_sram_shared_loops_in2buf_autovec_write_1_ranges),
  .cen_to_sram_top(strg_ub_cen_to_sram_top),
  .clk(strg_ub_clk),
  .clk_en(clk_en),
  .data_from_strg(mem_data_out),
  .data_in(data_in),
  .data_out_top(strg_ub_data_out_top),
  .data_to_sram_top(strg_ub_data_to_sram_top),
  .flush(flush),
  .loops_sram2tb_mux_sel_top(strg_ub_loops_sram2tb_mux_sel_top),
  .loops_sram2tb_restart_top(strg_ub_loops_sram2tb_restart_top),
  .rst_n(rst_n),
  .t_read_out_top(strg_ub_t_read_out_top),
  .wen_to_sram_top(strg_ub_wen_to_sram_top),
  .accessor_output(accessor_output),
  .addr_out(ub_addr_to_mem),
  .cen_to_strg(ub_cen_to_mem),
  .data_out(ub_data_out),
  .data_to_strg(ub_data_to_mem),
  .strg_ub_agg_data_out(formal_agg_data_out),
  .wen_to_strg(ub_wen_to_mem)
);

strg_ram sram_ctrl (
  .clk(sram_ctrl_clk),
  .clk_en(clk_en),
  .data_from_strg(mem_data_out),
  .data_in(sram_ctrl_data_in),
  .flush(flush),
  .rd_addr_in(sram_ctrl_rd_addr_in),
  .ren(sram_ctrl_ren),
  .rst_n(rst_n),
  .wen(sram_ctrl_wen),
  .wr_addr_in(sram_ctrl_wr_addr_in),
  .addr_out(sram_addr_to_mem),
  .data_out(sram_data_out),
  .data_to_strg(sram_data_to_mem),
  .ready(sram_ready_out),
  .ren_to_strg(sram_ren_to_mem),
  .valid_out(sram_valid_out),
  .wen_to_strg(sram_wen_to_mem)
);

strg_fifo fifo_ctrl (
  .clk(fifo_ctrl_clk),
  .clk_en(clk_en),
  .data_from_strg(mem_data_out),
  .data_in(fifo_ctrl_data_in),
  .fifo_depth(fifo_ctrl_fifo_depth),
  .flush(flush),
  .pop(fifo_ctrl_pop),
  .push(fifo_ctrl_push),
  .rst_n(rst_n),
  .addr_out(fifo_addr_to_mem),
  .data_out(fifo_data_out),
  .data_to_strg(fifo_data_to_mem),
  .empty(fifo_empty),
  .full(fifo_full),
  .ren_to_strg(fifo_ren_to_mem),
  .valid_out(fifo_valid_out),
  .wen_to_strg(fifo_wen_to_mem)
);

Chain chain (
  .accessor_output(chain_accessor_output),
  .chain_data_in(chain_data_in),
  .chain_en(chain_chain_en),
  .clk_en(clk_en),
  .curr_tile_data_out(data_out_tile),
  .flush(flush),
  .data_out_tile(data_out)
);

endmodule   // LakeTop

module addr_gen_6_16 (
  input logic clk,
  input logic clk_en,
  input logic flush,
  input logic [2:0] mux_sel,
  input logic restart,
  input logic rst_n,
  input logic [15:0] starting_addr,
  input logic step,
  input logic [5:0] [15:0] strides,
  output logic [15:0] addr_out
);

logic [15:0] calc_addr;
logic [15:0] current_addr;
logic [15:0] strt_addr;
assign strt_addr = starting_addr;
assign addr_out = calc_addr;
assign calc_addr = strt_addr + current_addr;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    current_addr <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      current_addr <= 16'h0;
    end
    else if (step) begin
      if (restart) begin
        current_addr <= 16'h0;
      end
      else current_addr <= current_addr + strides[mux_sel];
    end
  end
end
endmodule   // addr_gen_6_16

module addr_gen_6_4 (
  input logic clk,
  input logic clk_en,
  input logic flush,
  input logic [2:0] mux_sel,
  input logic restart,
  input logic rst_n,
  input logic [3:0] starting_addr,
  input logic step,
  input logic [5:0] [3:0] strides,
  output logic [3:0] addr_out
);

logic [3:0] calc_addr;
logic [3:0] current_addr;
logic [3:0] strt_addr;
assign strt_addr = starting_addr;
assign addr_out = calc_addr;
assign calc_addr = strt_addr + current_addr;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    current_addr <= 4'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      current_addr <= 4'h0;
    end
    else if (step) begin
      if (restart) begin
        current_addr <= 4'h0;
      end
      else current_addr <= current_addr + strides[mux_sel];
    end
  end
end
endmodule   // addr_gen_6_4

module for_loop_6_16 #(
  parameter CONFIG_WIDTH = 5'h10,
  parameter ITERATOR_SUPPORT = 4'h6
)
(
  input logic clk,
  input logic clk_en,
  input logic [3:0] dimensionality,
  input logic flush,
  input logic [5:0] [15:0] ranges,
  input logic rst_n,
  input logic step,
  output logic [2:0] mux_sel_out,
  output logic restart
);

logic [5:0] clear;
logic [5:0][15:0] dim_counter;
logic done;
logic [5:0] inc;
logic [15:0] inced_cnt;
logic [5:0] max_value;
logic maxed_value;
logic [2:0] mux_sel;
assign mux_sel_out = mux_sel;
assign inced_cnt = dim_counter[mux_sel] + 16'h1;
assign maxed_value = (dim_counter[mux_sel] == ranges[mux_sel]) & inc[mux_sel];
always_comb begin
  mux_sel = 3'h0;
  done = 1'h0;
  if (~done) begin
    if ((~max_value[0]) & (dimensionality > 4'h0)) begin
      mux_sel = 3'h0;
      done = 1'h1;
    end
  end
  if (~done) begin
    if ((~max_value[1]) & (dimensionality > 4'h1)) begin
      mux_sel = 3'h1;
      done = 1'h1;
    end
  end
  if (~done) begin
    if ((~max_value[2]) & (dimensionality > 4'h2)) begin
      mux_sel = 3'h2;
      done = 1'h1;
    end
  end
  if (~done) begin
    if ((~max_value[3]) & (dimensionality > 4'h3)) begin
      mux_sel = 3'h3;
      done = 1'h1;
    end
  end
  if (~done) begin
    if ((~max_value[4]) & (dimensionality > 4'h4)) begin
      mux_sel = 3'h4;
      done = 1'h1;
    end
  end
  if (~done) begin
    if ((~max_value[5]) & (dimensionality > 4'h5)) begin
      mux_sel = 3'h5;
      done = 1'h1;
    end
  end
end
always_comb begin
  clear[0] = 1'h0;
  if (((mux_sel > 3'h0) | (~done)) & step) begin
    clear[0] = 1'h1;
  end
end
always_comb begin
  inc[0] = 1'h0;
  if ((5'h0 == 5'h0) & step & (dimensionality > 4'h0)) begin
    inc[0] = 1'h1;
  end
  else if ((mux_sel == 3'h0) & step & (dimensionality > 4'h0)) begin
    inc[0] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[0] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[0] <= 16'h0;
    end
    else if (clear[0]) begin
      dim_counter[0] <= 16'h0;
    end
    else if (inc[0]) begin
      dim_counter[0] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[0] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[0] <= 1'h0;
    end
    else if (clear[0]) begin
      max_value[0] <= 1'h0;
    end
    else if (inc[0]) begin
      max_value[0] <= maxed_value;
    end
  end
end
always_comb begin
  clear[1] = 1'h0;
  if (((mux_sel > 3'h1) | (~done)) & step) begin
    clear[1] = 1'h1;
  end
end
always_comb begin
  inc[1] = 1'h0;
  if ((5'h1 == 5'h0) & step & (dimensionality > 4'h1)) begin
    inc[1] = 1'h1;
  end
  else if ((mux_sel == 3'h1) & step & (dimensionality > 4'h1)) begin
    inc[1] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[1] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[1] <= 16'h0;
    end
    else if (clear[1]) begin
      dim_counter[1] <= 16'h0;
    end
    else if (inc[1]) begin
      dim_counter[1] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[1] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[1] <= 1'h0;
    end
    else if (clear[1]) begin
      max_value[1] <= 1'h0;
    end
    else if (inc[1]) begin
      max_value[1] <= maxed_value;
    end
  end
end
always_comb begin
  clear[2] = 1'h0;
  if (((mux_sel > 3'h2) | (~done)) & step) begin
    clear[2] = 1'h1;
  end
end
always_comb begin
  inc[2] = 1'h0;
  if ((5'h2 == 5'h0) & step & (dimensionality > 4'h2)) begin
    inc[2] = 1'h1;
  end
  else if ((mux_sel == 3'h2) & step & (dimensionality > 4'h2)) begin
    inc[2] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[2] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[2] <= 16'h0;
    end
    else if (clear[2]) begin
      dim_counter[2] <= 16'h0;
    end
    else if (inc[2]) begin
      dim_counter[2] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[2] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[2] <= 1'h0;
    end
    else if (clear[2]) begin
      max_value[2] <= 1'h0;
    end
    else if (inc[2]) begin
      max_value[2] <= maxed_value;
    end
  end
end
always_comb begin
  clear[3] = 1'h0;
  if (((mux_sel > 3'h3) | (~done)) & step) begin
    clear[3] = 1'h1;
  end
end
always_comb begin
  inc[3] = 1'h0;
  if ((5'h3 == 5'h0) & step & (dimensionality > 4'h3)) begin
    inc[3] = 1'h1;
  end
  else if ((mux_sel == 3'h3) & step & (dimensionality > 4'h3)) begin
    inc[3] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[3] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[3] <= 16'h0;
    end
    else if (clear[3]) begin
      dim_counter[3] <= 16'h0;
    end
    else if (inc[3]) begin
      dim_counter[3] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[3] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[3] <= 1'h0;
    end
    else if (clear[3]) begin
      max_value[3] <= 1'h0;
    end
    else if (inc[3]) begin
      max_value[3] <= maxed_value;
    end
  end
end
always_comb begin
  clear[4] = 1'h0;
  if (((mux_sel > 3'h4) | (~done)) & step) begin
    clear[4] = 1'h1;
  end
end
always_comb begin
  inc[4] = 1'h0;
  if ((5'h4 == 5'h0) & step & (dimensionality > 4'h4)) begin
    inc[4] = 1'h1;
  end
  else if ((mux_sel == 3'h4) & step & (dimensionality > 4'h4)) begin
    inc[4] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[4] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[4] <= 16'h0;
    end
    else if (clear[4]) begin
      dim_counter[4] <= 16'h0;
    end
    else if (inc[4]) begin
      dim_counter[4] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[4] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[4] <= 1'h0;
    end
    else if (clear[4]) begin
      max_value[4] <= 1'h0;
    end
    else if (inc[4]) begin
      max_value[4] <= maxed_value;
    end
  end
end
always_comb begin
  clear[5] = 1'h0;
  if (((mux_sel > 3'h5) | (~done)) & step) begin
    clear[5] = 1'h1;
  end
end
always_comb begin
  inc[5] = 1'h0;
  if ((5'h5 == 5'h0) & step & (dimensionality > 4'h5)) begin
    inc[5] = 1'h1;
  end
  else if ((mux_sel == 3'h5) & step & (dimensionality > 4'h5)) begin
    inc[5] = 1'h1;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    dim_counter[5] <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      dim_counter[5] <= 16'h0;
    end
    else if (clear[5]) begin
      dim_counter[5] <= 16'h0;
    end
    else if (inc[5]) begin
      dim_counter[5] <= inced_cnt;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    max_value[5] <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      max_value[5] <= 1'h0;
    end
    else if (clear[5]) begin
      max_value[5] <= 1'h0;
    end
    else if (inc[5]) begin
      max_value[5] <= maxed_value;
    end
  end
end
assign restart = step & (~done);
endmodule   // for_loop_6_16

module reg_fifo_d_4_w_1 #(
  parameter data_width = 16'h10
)
(
  input logic clk,
  input logic clk_en,
  input logic [0:0] [data_width-1:0] data_in,
  input logic flush,
  input logic [2:0] num_load,
  input logic [3:0][0:0] [data_width-1:0] parallel_in,
  input logic parallel_load,
  input logic parallel_read,
  input logic pop,
  input logic push,
  input logic rst_n,
  output logic [0:0] [data_width-1:0] data_out,
  output logic empty,
  output logic full,
  output logic [3:0][0:0] [data_width-1:0] parallel_out,
  output logic [1:0] rd_ptr_out,
  output logic valid
);

logic [2:0] num_items;
logic passthru;
logic [1:0] rd_ptr;
logic read;
logic [3:0][0:0][data_width-1:0] reg_array;
logic [1:0] wr_ptr;
logic write;
assign rd_ptr_out = rd_ptr;
assign full = num_items == 3'h4;
assign empty = num_items == 3'h0;
assign read = pop & (~passthru) & (~empty);
assign passthru = pop & push & empty;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    num_items <= 3'h0;
  end
  else if (flush) begin
    num_items <= 3'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      if (num_load == 3'h0) begin
        num_items <= 3'(push);
      end
      else num_items <= num_load;
    end
    else if (parallel_read) begin
      if (push) begin
        num_items <= 3'h1;
      end
      else num_items <= 3'h0;
    end
    else if (write & (~read)) begin
      num_items <= num_items + 3'h1;
    end
    else if ((~write) & read) begin
      num_items <= num_items - 3'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    reg_array <= 64'h0;
  end
  else if (flush) begin
    reg_array <= 64'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      reg_array <= parallel_in;
    end
    else if (write) begin
      if (parallel_read) begin
        reg_array[0] <= data_in;
      end
      else reg_array[wr_ptr] <= data_in;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    wr_ptr <= 2'h0;
  end
  else if (flush) begin
    wr_ptr <= 2'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      wr_ptr <= num_load[1:0];
    end
    else if (parallel_read) begin
      if (push) begin
        wr_ptr <= 2'h1;
      end
      else wr_ptr <= 2'h0;
    end
    else if (write) begin
      wr_ptr <= wr_ptr + 2'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    rd_ptr <= 2'h0;
  end
  else if (flush) begin
    rd_ptr <= 2'h0;
  end
  else if (clk_en) begin
    if (parallel_load | parallel_read) begin
      rd_ptr <= 2'h0;
    end
    else if (read) begin
      rd_ptr <= rd_ptr + 2'h1;
    end
  end
end
assign parallel_out = reg_array;
assign write = push & (~passthru) & ((~full) | pop | parallel_read);
always_comb begin
  if (passthru) begin
    data_out = data_in;
  end
  else data_out = reg_array[rd_ptr];
end
always_comb begin
  valid = pop & ((~empty) | passthru);
end
endmodule   // reg_fifo_d_4_w_1

module reg_fifo_d_4_w_1_unq0 #(
  parameter data_width = 16'h10
)
(
  input logic clk,
  input logic clk_en,
  input logic [0:0] [data_width-1:0] data_in,
  input logic flush,
  input logic [2:0] num_load,
  input logic [3:0][0:0] [data_width-1:0] parallel_in,
  input logic parallel_load,
  input logic parallel_read,
  input logic pop,
  input logic push,
  input logic rst_n,
  output logic [0:0] [data_width-1:0] data_out,
  output logic empty,
  output logic full,
  output logic [3:0][0:0] [data_width-1:0] parallel_out,
  output logic valid
);

logic [2:0] num_items;
logic passthru;
logic [1:0] rd_ptr;
logic read;
logic [3:0][0:0][data_width-1:0] reg_array;
logic [1:0] wr_ptr;
logic write;
assign full = num_items == 3'h4;
assign empty = num_items == 3'h0;
assign read = pop & (~passthru) & (~empty);
assign passthru = pop & push & empty;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    num_items <= 3'h0;
  end
  else if (flush) begin
    num_items <= 3'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      if (num_load == 3'h0) begin
        num_items <= 3'(push);
      end
      else num_items <= num_load;
    end
    else if (parallel_read) begin
      if (push) begin
        num_items <= 3'h1;
      end
      else num_items <= 3'h0;
    end
    else if (write & (~read)) begin
      num_items <= num_items + 3'h1;
    end
    else if ((~write) & read) begin
      num_items <= num_items - 3'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    reg_array <= 64'h0;
  end
  else if (flush) begin
    reg_array <= 64'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      reg_array <= parallel_in;
    end
    else if (write) begin
      if (parallel_read) begin
        reg_array[0] <= data_in;
      end
      else reg_array[wr_ptr] <= data_in;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    wr_ptr <= 2'h0;
  end
  else if (flush) begin
    wr_ptr <= 2'h0;
  end
  else if (clk_en) begin
    if (parallel_load) begin
      wr_ptr <= num_load[1:0];
    end
    else if (parallel_read) begin
      if (push) begin
        wr_ptr <= 2'h1;
      end
      else wr_ptr <= 2'h0;
    end
    else if (write) begin
      wr_ptr <= wr_ptr + 2'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    rd_ptr <= 2'h0;
  end
  else if (flush) begin
    rd_ptr <= 2'h0;
  end
  else if (clk_en) begin
    if (parallel_load | parallel_read) begin
      rd_ptr <= 2'h0;
    end
    else if (read) begin
      rd_ptr <= rd_ptr + 2'h1;
    end
  end
end
assign parallel_out = reg_array;
assign write = push & (~passthru) & ((~full) | pop | parallel_read);
always_comb begin
  if (passthru) begin
    data_out = data_in;
  end
  else data_out = reg_array[rd_ptr];
end
always_comb begin
  valid = pop & ((~empty) | passthru);
end
endmodule   // reg_fifo_d_4_w_1_unq0

module sched_gen_6_16 (
  input logic clk,
  input logic clk_en,
  input logic [15:0] cycle_count,
  input logic enable,
  input logic finished,
  input logic flush,
  input logic [2:0] mux_sel,
  input logic rst_n,
  input logic [15:0] sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] sched_addr_gen_strides,
  output logic valid_output
);

logic [15:0] addr_out;
logic valid_gate;
logic valid_gate_inv;
logic valid_out;
assign valid_gate = ~valid_gate_inv;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    valid_gate_inv <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      valid_gate_inv <= 1'h0;
    end
    else if (finished) begin
      valid_gate_inv <= 1'h1;
    end
  end
end
always_comb begin
  valid_out = (cycle_count == addr_out) & valid_gate & enable;
end
always_comb begin
  valid_output = valid_out;
end
addr_gen_6_16 sched_addr_gen (
  .clk(clk),
  .clk_en(clk_en),
  .flush(flush),
  .mux_sel(mux_sel),
  .restart(1'h0),
  .rst_n(rst_n),
  .starting_addr(sched_addr_gen_starting_addr),
  .step(valid_out),
  .strides(sched_addr_gen_strides),
  .addr_out(addr_out)
);

endmodule   // sched_gen_6_16

module storage_config_seq (
  input logic clk,
  input logic clk_en,
  input logic [7:0] config_addr_in,
  input logic [15:0] config_data_in,
  input logic [1:0] config_en,
  input logic config_rd,
  input logic config_wr,
  input logic flush,
  input logic [0:0][3:0] [15:0] rd_data_stg,
  input logic rst_n,
  output logic [8:0] addr_out,
  output logic [1:0] [15:0] rd_data_out,
  output logic ren_out,
  output logic wen_out,
  output logic [3:0] [15:0] wr_data
);

logic [1:0] cnt;
logic [2:0][15:0] data_wr_reg;
logic [1:0] rd_cnt;
logic [1:0] reduce_en;
logic set_to_addr;
assign reduce_en[0] = |config_en[0];
assign reduce_en[1] = |config_en[1];
always_comb begin
  set_to_addr = 1'h0;
  for (int unsigned i = 0; i < 2; i += 1) begin
      if (reduce_en[1'(i)]) begin
        set_to_addr = 1'(i);
      end
    end
end
assign addr_out = {set_to_addr, config_addr_in};

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    cnt <= 2'h0;
  end
  else if (flush) begin
    cnt <= 2'h0;
  end
  else if (clk_en) begin
    if ((config_wr | config_rd) & (|config_en)) begin
      cnt <= cnt + 2'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    rd_cnt <= 2'h0;
  end
  else if (flush) begin
    rd_cnt <= 2'h0;
  end
  else if (clk_en) begin
    rd_cnt <= cnt;
  end
end
assign rd_data_out[0] = rd_data_stg[0][rd_cnt];
assign rd_data_out[1] = rd_data_stg[0][rd_cnt];

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    data_wr_reg <= 48'h0;
  end
  else if (flush) begin
    data_wr_reg <= 48'h0;
  end
  else if (clk_en) begin
    if (config_wr & (cnt < 2'h3)) begin
      data_wr_reg[cnt] <= config_data_in;
    end
  end
end
assign wr_data[0] = data_wr_reg[0];
assign wr_data[1] = data_wr_reg[1];
assign wr_data[2] = data_wr_reg[2];
assign wr_data[3] = config_data_in;
assign wen_out = config_wr & (cnt == 2'h3);
assign ren_out = config_rd;
endmodule   // storage_config_seq

module strg_fifo (
  input logic clk,
  input logic clk_en,
  input logic [0:0][3:0] [15:0] data_from_strg,
  input logic [15:0] data_in,
  input logic [15:0] fifo_depth,
  input logic flush,
  input logic pop,
  input logic push,
  input logic rst_n,
  output logic [0:0] [8:0] addr_out,
  output logic [15:0] data_out,
  output logic [0:0][3:0] [15:0] data_to_strg,
  output logic empty,
  output logic full,
  output logic ren_to_strg,
  output logic valid_out,
  output logic wen_to_strg
);

logic [15:0] back_data_in;
logic [15:0] back_data_out;
logic back_empty;
logic back_full;
logic [2:0] back_num_load;
logic [2:0] back_occ;
logic [3:0][0:0][15:0] back_par_in;
logic back_pl;
logic back_pop;
logic back_push;
logic [0:0][15:0] back_rf_data_in;
logic [0:0][15:0] back_rf_data_out;
logic back_rf_parallel_load;
logic back_valid;
logic curr_bank_rd;
logic curr_bank_wr;
logic [3:0][15:0] front_combined;
logic [15:0] front_data_out;
logic front_empty;
logic front_full;
logic [2:0] front_occ;
logic [3:0][0:0][15:0] front_par_out;
logic front_par_read;
logic front_pop;
logic front_push;
logic [1:0] front_rd_ptr;
logic [0:0][15:0] front_rf_data_in;
logic [0:0][15:0] front_rf_data_out;
logic front_valid;
logic fw_is_1;
logic [15:0] num_items;
logic [15:0] num_words_mem;
logic prev_bank_rd;
logic queued_write;
logic [0:0][8:0] ren_addr;
logic ren_delay;
logic [0:0][8:0] wen_addr;
logic [0:0][3:0][15:0] write_queue;
assign curr_bank_wr = 1'h0;
assign curr_bank_rd = 1'h0;
assign front_push = push & ((~full) | pop);
assign front_rf_data_in[0] = data_in;
assign front_data_out = front_rf_data_out[0];
assign fw_is_1 = 1'h0;
assign back_pop = pop & ((~empty) | push);
assign back_rf_parallel_load = back_pl & (|back_num_load);
assign back_rf_data_in[0] = back_data_in;
assign back_data_out = back_rf_data_out[0];
always_comb begin
  wen_to_strg = ((~ren_to_strg) | 1'h0) & (queued_write | ((front_occ == 3'h4) & push &
      (~front_pop) & (curr_bank_wr == 1'h0)));
end
always_comb begin
  ren_to_strg = ((back_occ == 3'h1) | fw_is_1) & (curr_bank_rd == 1'h0) & (pop | ((back_occ ==
      3'h0) & (back_num_load == 3'h0))) & ((num_words_mem > 16'h1) | ((num_words_mem
      == 16'h1) & (~back_pl)));
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    ren_delay <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      ren_delay <= 1'h0;
    end
    else ren_delay <= |ren_to_strg;
  end
end
assign back_pl = ren_delay;
assign front_combined[0] = front_par_out[front_rd_ptr + 2'h0];
assign front_combined[1] = front_par_out[front_rd_ptr + 2'h1];
assign front_combined[2] = front_par_out[front_rd_ptr + 2'h2];
assign front_combined[3] = front_par_out[front_rd_ptr + 2'h3];
assign data_to_strg[0] = queued_write ? write_queue[0]: front_combined;
assign back_data_in = front_data_out;
assign back_push = front_valid;
always_comb begin
  front_pop = ((num_words_mem == 16'h0) | ((num_words_mem == 16'h1) & back_pl)) & ((~back_pl)
      | (back_pl & (back_num_load == 3'h0))) & ((~(back_occ == 3'h4)) | pop) &
      ((~(front_occ == 3'h0)) | push);
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    write_queue[0] <= 64'h0;
    queued_write <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      write_queue[0] <= 64'h0;
      queued_write <= 1'h0;
    end
    else if (front_par_read & (~wen_to_strg) & (curr_bank_wr == 1'h0)) begin
      write_queue[0] <= front_combined;
      queued_write <= 1'h1;
    end
    else if (wen_to_strg) begin
      queued_write <= 1'h0;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    num_words_mem <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      num_words_mem <= 16'h0;
    end
    else if ((~back_pl) & front_par_read) begin
      num_words_mem <= num_words_mem + 16'h1;
    end
    else if (back_pl & (~front_par_read)) begin
      num_words_mem <= num_words_mem - 16'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    front_occ <= 3'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      front_occ <= 3'h0;
    end
    else if (front_par_read) begin
      if (front_push) begin
        front_occ <= 3'h1;
      end
      else front_occ <= 3'h0;
    end
    else if (front_push & (~front_pop)) begin
      front_occ <= front_occ + 3'h1;
    end
    else if ((~front_push) & front_pop) begin
      front_occ <= front_occ - 3'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    back_occ <= 3'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      back_occ <= 3'h0;
    end
    else if (back_pl) begin
      if (back_num_load == 3'h0) begin
        back_occ <= 3'(back_push);
      end
      else back_occ <= back_num_load;
    end
    else if (back_push & (~back_pop)) begin
      back_occ <= back_occ + 3'h1;
    end
    else if ((~back_push) & back_pop) begin
      back_occ <= back_occ - 3'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    prev_bank_rd <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      prev_bank_rd <= 1'h0;
    end
    else prev_bank_rd <= curr_bank_rd;
  end
end
assign back_par_in[0] = (back_num_load == 3'h4) ? data_from_strg[prev_bank_rd][0]:
    data_from_strg[prev_bank_rd][1];
assign back_par_in[1] = (back_num_load == 3'h4) ? data_from_strg[prev_bank_rd][1]:
    data_from_strg[prev_bank_rd][2];
assign back_par_in[2] = (back_num_load == 3'h4) ? data_from_strg[prev_bank_rd][2]:
    data_from_strg[prev_bank_rd][3];
assign back_par_in[3] = (back_num_load == 3'h4) ? data_from_strg[prev_bank_rd][3]: 16'h0;
always_comb begin
  front_par_read = (front_occ == 3'h4) & push & (~front_pop);
end
always_comb begin
  if (back_pl) begin
    back_num_load = pop ? 3'h3: 3'h4;
  end
  else back_num_load = 3'h0;
end
assign data_out = back_pl ? data_from_strg[prev_bank_rd][0]: back_data_out;
assign valid_out = back_pl ? pop: back_valid;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    wen_addr[0] <= 9'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      wen_addr[0] <= 9'h0;
    end
    else if (wen_to_strg) begin
      wen_addr[0] <= wen_addr[0] + 9'h1;
    end
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    ren_addr[0] <= 9'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      ren_addr[0] <= 9'h0;
    end
    else if (ren_to_strg) begin
      ren_addr[0] <= ren_addr[0] + 9'h1;
    end
  end
end
assign addr_out[0] = wen_to_strg ? wen_addr[0]: ren_addr[0];
always_comb begin
  num_items = 16'(num_words_mem * 16'h4) + 16'(front_occ) + 16'(back_occ);
end
assign empty = num_items == 16'h0;
assign full = fifo_depth == num_items;
reg_fifo_d_4_w_1 #(
  .data_width(16'h10))
front_rf (
  .clk(clk),
  .clk_en(clk_en),
  .data_in(front_rf_data_in),
  .flush(flush),
  .num_load(3'h0),
  .parallel_in(64'h0),
  .parallel_load(1'h0),
  .parallel_read(front_par_read),
  .pop(front_pop),
  .push(front_push),
  .rst_n(rst_n),
  .data_out(front_rf_data_out),
  .empty(front_empty),
  .full(front_full),
  .parallel_out(front_par_out),
  .rd_ptr_out(front_rd_ptr),
  .valid(front_valid)
);

reg_fifo_d_4_w_1_unq0 #(
  .data_width(16'h10))
back_rf (
  .clk(clk),
  .clk_en(clk_en),
  .data_in(back_rf_data_in),
  .flush(flush),
  .num_load(back_num_load),
  .parallel_in(back_par_in),
  .parallel_load(back_rf_parallel_load),
  .parallel_read(1'h0),
  .pop(back_pop),
  .push(back_push),
  .rst_n(rst_n),
  .data_out(back_rf_data_out),
  .empty(back_empty),
  .full(back_full),
  .valid(back_valid)
);

endmodule   // strg_fifo

module strg_ram (
  input logic clk,
  input logic clk_en,
  input logic [0:0][3:0] [15:0] data_from_strg,
  input logic [15:0] data_in,
  input logic flush,
  input logic [15:0] rd_addr_in,
  input logic ren,
  input logic rst_n,
  input logic wen,
  input logic [15:0] wr_addr_in,
  output logic [0:0] [8:0] addr_out,
  output logic [15:0] data_out,
  output logic [0:0][3:0] [15:0] data_to_strg,
  output logic ready,
  output logic ren_to_strg,
  output logic valid_out,
  output logic wen_to_strg
);

typedef enum logic[1:0] {
  IDLE = 2'h0,
  MODIFY = 2'h1,
  READ = 2'h2,
  _DEFAULT = 2'h3
} r_w_seq_state;
logic [15:0] addr_to_write;
logic [3:0][15:0] data_combined;
logic [15:0] data_to_write;
r_w_seq_state r_w_seq_current_state;
r_w_seq_state r_w_seq_next_state;
logic [15:0] rd_addr;
logic rd_bank;
logic rd_valid;
logic read_gate;
logic [15:0] wr_addr;
logic write_gate;
assign wr_addr = wr_addr_in;
assign rd_addr = wr_addr_in;
assign rd_bank = 1'h0;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    rd_valid <= 1'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      rd_valid <= 1'h0;
    end
    else rd_valid <= ren & (~wen);
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    data_to_write <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      data_to_write <= 16'h0;
    end
    else data_to_write <= data_in;
  end
end

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    addr_to_write <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      addr_to_write <= 16'h0;
    end
    else addr_to_write <= wr_addr;
  end
end
assign data_to_strg[0] = data_combined;
assign ren_to_strg = (wen | ren) & read_gate;
assign wen_to_strg = write_gate;
always_comb begin
  addr_out[0] = rd_addr[10:2];
  if (wen & (~write_gate)) begin
    addr_out[0] = wr_addr[10:2];
  end
  else if (write_gate) begin
    addr_out[0] = addr_to_write[10:2];
  end
end
always_comb begin
  if (addr_to_write[1:0] == 2'h0) begin
    data_combined[0] = data_to_write;
  end
  else data_combined[0] = data_from_strg[rd_bank][0];
end
always_comb begin
  if (addr_to_write[1:0] == 2'h1) begin
    data_combined[1] = data_to_write;
  end
  else data_combined[1] = data_from_strg[rd_bank][1];
end
always_comb begin
  if (addr_to_write[1:0] == 2'h2) begin
    data_combined[2] = data_to_write;
  end
  else data_combined[2] = data_from_strg[rd_bank][2];
end
always_comb begin
  if (addr_to_write[1:0] == 2'h3) begin
    data_combined[3] = data_to_write;
  end
  else data_combined[3] = data_from_strg[rd_bank][3];
end

always_ff @(posedge clk, negedge rst_n) begin
  if (!rst_n) begin
    r_w_seq_current_state <= IDLE;
  end
  else r_w_seq_current_state <= r_w_seq_next_state;
end
always_comb begin
  r_w_seq_next_state = r_w_seq_current_state;
  unique case (r_w_seq_current_state)
    IDLE: begin
        if ((~wen) & (~ren)) begin
          r_w_seq_next_state = IDLE;
        end
        else if (wen) begin
          r_w_seq_next_state = MODIFY;
        end
        else if (ren & (~wen)) begin
          r_w_seq_next_state = READ;
        end
      end
    MODIFY: begin
        if (1'h1) begin
          r_w_seq_next_state = IDLE;
        end
      end
    READ: begin
        if ((~wen) & (~ren)) begin
          r_w_seq_next_state = IDLE;
        end
        else if (wen) begin
          r_w_seq_next_state = MODIFY;
        end
        else if (ren & (~wen)) begin
          r_w_seq_next_state = READ;
        end
      end
    _DEFAULT: begin
        if (1'h1) begin
          r_w_seq_next_state = _DEFAULT;
        end
      end
  endcase
end
always_comb begin
  unique case (r_w_seq_current_state)
    IDLE: begin :r_w_seq_IDLE_Output
        data_out = 16'h0;
        read_gate = 1'h1;
        ready = 1'h1;
        valid_out = 1'h0;
        write_gate = 1'h0;
      end :r_w_seq_IDLE_Output
    MODIFY: begin :r_w_seq_MODIFY_Output
        data_out = 16'h0;
        read_gate = 1'h0;
        ready = 1'h0;
        valid_out = 1'h0;
        write_gate = 1'h1;
      end :r_w_seq_MODIFY_Output
    READ: begin :r_w_seq_READ_Output
        data_out = data_from_strg[rd_bank][addr_to_write[1:0]];
        read_gate = 1'h1;
        ready = 1'h1;
        valid_out = 1'h1;
        write_gate = 1'h0;
      end :r_w_seq_READ_Output
    _DEFAULT: begin :r_w_seq__DEFAULT_Output
        data_out = 16'h0;
        read_gate = 1'h0;
        ready = 1'h0;
        valid_out = 1'h0;
        write_gate = 1'h0;
      end :r_w_seq__DEFAULT_Output
  endcase
end
endmodule   // strg_ram

module strg_ub_agg_only (
  input logic [1:0] agg_read,
  input logic [3:0] agg_read_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] agg_read_addr_gen_0_strides,
  input logic [3:0] agg_read_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] agg_read_addr_gen_1_strides,
  input logic [3:0] agg_write_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] agg_write_addr_gen_0_strides,
  input logic [3:0] agg_write_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] agg_write_addr_gen_1_strides,
  input logic agg_write_sched_gen_0_enable,
  input logic [15:0] agg_write_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_write_sched_gen_0_sched_addr_gen_strides,
  input logic agg_write_sched_gen_1_enable,
  input logic [15:0] agg_write_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_write_sched_gen_1_sched_addr_gen_strides,
  input logic clk,
  input logic clk_en,
  input logic [15:0] cycle_count,
  input logic [1:0] [15:0] data_in,
  input logic [1:0] [2:0] floop_mux_sel,
  input logic [1:0] floop_restart,
  input logic flush,
  input logic [3:0] loops_in2buf_0_dimensionality,
  input logic [5:0] [15:0] loops_in2buf_0_ranges,
  input logic [3:0] loops_in2buf_1_dimensionality,
  input logic [5:0] [15:0] loops_in2buf_1_ranges,
  input logic rst_n,
  output logic [1:0][3:0] [15:0] agg_data_out
);

logic [1:0][3:0][3:0][15:0] agg;
logic [1:0][1:0] agg_read_addr;
logic [3:0] agg_read_addr_gen_0_addr_out;
logic [2:0] agg_read_addr_gen_0_mux_sel;
logic agg_read_addr_gen_0_restart;
logic agg_read_addr_gen_0_step;
logic [3:0] agg_read_addr_gen_1_addr_out;
logic [2:0] agg_read_addr_gen_1_mux_sel;
logic agg_read_addr_gen_1_restart;
logic agg_read_addr_gen_1_step;
logic [1:0][7:0] agg_read_addr_gen_out;
logic [1:0] agg_write;
logic [1:0][3:0] agg_write_addr;
logic [3:0] agg_write_addr_gen_0_addr_out;
logic agg_write_addr_gen_0_step;
logic [3:0] agg_write_addr_gen_1_addr_out;
logic agg_write_addr_gen_1_step;
logic agg_write_sched_gen_0_valid_output;
logic agg_write_sched_gen_1_valid_output;
logic [2:0] loops_in2buf_0_mux_sel_out;
logic loops_in2buf_0_restart;
logic loops_in2buf_0_step;
logic [2:0] loops_in2buf_1_mux_sel_out;
logic loops_in2buf_1_restart;
logic loops_in2buf_1_step;
assign loops_in2buf_0_step = agg_write[0];
assign agg_write_addr_gen_0_step = agg_write[0];
assign agg_write_addr[0] = agg_write_addr_gen_0_addr_out;
assign agg_write[0] = agg_write_sched_gen_0_valid_output;

always_ff @(posedge clk) begin
  if (clk_en) begin
    if (agg_write[0]) begin
      agg[0][agg_write_addr[0][3:2]][agg_write_addr[0][1:0]] <= data_in[0];
    end
  end
end
assign agg_read_addr_gen_0_step = agg_read[0];
assign agg_read_addr_gen_0_restart = floop_restart[0];
assign agg_read_addr_gen_0_mux_sel = floop_mux_sel[0];
assign agg_read_addr_gen_out[0][3:0] = agg_read_addr_gen_0_addr_out;
assign agg_read_addr_gen_out[0][7:4] = 4'h0;
assign agg_read_addr[0] = agg_read_addr_gen_out[0][1:0];
always_comb begin
  agg_data_out[0] = agg[0][agg_read_addr[0]];
end
assign loops_in2buf_1_step = agg_write[1];
assign agg_write_addr_gen_1_step = agg_write[1];
assign agg_write_addr[1] = agg_write_addr_gen_1_addr_out;
assign agg_write[1] = agg_write_sched_gen_1_valid_output;

always_ff @(posedge clk) begin
  if (clk_en) begin
    if (agg_write[1]) begin
      agg[1][agg_write_addr[1][3:2]][agg_write_addr[1][1:0]] <= data_in[1];
    end
  end
end
assign agg_read_addr_gen_1_step = agg_read[1];
assign agg_read_addr_gen_1_restart = floop_restart[1];
assign agg_read_addr_gen_1_mux_sel = floop_mux_sel[1];
assign agg_read_addr_gen_out[1][3:0] = agg_read_addr_gen_1_addr_out;
assign agg_read_addr_gen_out[1][7:4] = 4'h0;
assign agg_read_addr[1] = agg_read_addr_gen_out[1][1:0];
always_comb begin
  agg_data_out[1] = agg[1][agg_read_addr[1]];
end
for_loop_6_16 #(
  .CONFIG_WIDTH(5'h10),
  .ITERATOR_SUPPORT(4'h6))
loops_in2buf_0 (
  .clk(clk),
  .clk_en(clk_en),
  .dimensionality(loops_in2buf_0_dimensionality),
  .flush(flush),
  .ranges(loops_in2buf_0_ranges),
  .rst_n(rst_n),
  .step(loops_in2buf_0_step),
  .mux_sel_out(loops_in2buf_0_mux_sel_out),
  .restart(loops_in2buf_0_restart)
);

addr_gen_6_4 agg_write_addr_gen_0 (
  .clk(clk),
  .clk_en(clk_en),
  .flush(flush),
  .mux_sel(loops_in2buf_0_mux_sel_out),
  .restart(loops_in2buf_0_restart),
  .rst_n(rst_n),
  .starting_addr(agg_write_addr_gen_0_starting_addr),
  .step(agg_write_addr_gen_0_step),
  .strides(agg_write_addr_gen_0_strides),
  .addr_out(agg_write_addr_gen_0_addr_out)
);

sched_gen_6_16 agg_write_sched_gen_0 (
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .enable(agg_write_sched_gen_0_enable),
  .finished(loops_in2buf_0_restart),
  .flush(flush),
  .mux_sel(loops_in2buf_0_mux_sel_out),
  .rst_n(rst_n),
  .sched_addr_gen_starting_addr(agg_write_sched_gen_0_sched_addr_gen_starting_addr),
  .sched_addr_gen_strides(agg_write_sched_gen_0_sched_addr_gen_strides),
  .valid_output(agg_write_sched_gen_0_valid_output)
);

addr_gen_6_4 agg_read_addr_gen_0 (
  .clk(clk),
  .clk_en(clk_en),
  .flush(flush),
  .mux_sel(agg_read_addr_gen_0_mux_sel),
  .restart(agg_read_addr_gen_0_restart),
  .rst_n(rst_n),
  .starting_addr(agg_read_addr_gen_0_starting_addr),
  .step(agg_read_addr_gen_0_step),
  .strides(agg_read_addr_gen_0_strides),
  .addr_out(agg_read_addr_gen_0_addr_out)
);

for_loop_6_16 #(
  .CONFIG_WIDTH(5'h10),
  .ITERATOR_SUPPORT(4'h6))
loops_in2buf_1 (
  .clk(clk),
  .clk_en(clk_en),
  .dimensionality(loops_in2buf_1_dimensionality),
  .flush(flush),
  .ranges(loops_in2buf_1_ranges),
  .rst_n(rst_n),
  .step(loops_in2buf_1_step),
  .mux_sel_out(loops_in2buf_1_mux_sel_out),
  .restart(loops_in2buf_1_restart)
);

addr_gen_6_4 agg_write_addr_gen_1 (
  .clk(clk),
  .clk_en(clk_en),
  .flush(flush),
  .mux_sel(loops_in2buf_1_mux_sel_out),
  .restart(loops_in2buf_1_restart),
  .rst_n(rst_n),
  .starting_addr(agg_write_addr_gen_1_starting_addr),
  .step(agg_write_addr_gen_1_step),
  .strides(agg_write_addr_gen_1_strides),
  .addr_out(agg_write_addr_gen_1_addr_out)
);

sched_gen_6_16 agg_write_sched_gen_1 (
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .enable(agg_write_sched_gen_1_enable),
  .finished(loops_in2buf_1_restart),
  .flush(flush),
  .mux_sel(loops_in2buf_1_mux_sel_out),
  .rst_n(rst_n),
  .sched_addr_gen_starting_addr(agg_write_sched_gen_1_sched_addr_gen_starting_addr),
  .sched_addr_gen_strides(agg_write_sched_gen_1_sched_addr_gen_strides),
  .valid_output(agg_write_sched_gen_1_valid_output)
);

addr_gen_6_4 agg_read_addr_gen_1 (
  .clk(clk),
  .clk_en(clk_en),
  .flush(flush),
  .mux_sel(agg_read_addr_gen_1_mux_sel),
  .restart(agg_read_addr_gen_1_restart),
  .rst_n(rst_n),
  .starting_addr(agg_read_addr_gen_1_starting_addr),
  .step(agg_read_addr_gen_1_step),
  .strides(agg_read_addr_gen_1_strides),
  .addr_out(agg_read_addr_gen_1_addr_out)
);

endmodule   // strg_ub_agg_only

module strg_ub_agg_sram_shared (
  input logic agg_read_sched_gen_0_enable,
  input logic [15:0] agg_read_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_read_sched_gen_0_sched_addr_gen_strides,
  input logic agg_read_sched_gen_1_enable,
  input logic [15:0] agg_read_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_read_sched_gen_1_sched_addr_gen_strides,
  input logic clk,
  input logic clk_en,
  input logic [15:0] cycle_count,
  input logic flush,
  input logic [3:0] loops_in2buf_autovec_write_0_dimensionality,
  input logic [5:0] [15:0] loops_in2buf_autovec_write_0_ranges,
  input logic [3:0] loops_in2buf_autovec_write_1_dimensionality,
  input logic [5:0] [15:0] loops_in2buf_autovec_write_1_ranges,
  input logic rst_n,
  output logic [1:0] agg_read_out,
  output logic [1:0] [2:0] floop_mux_sel,
  output logic [1:0] floop_restart
);

logic [1:0] agg_read;
logic agg_read_sched_gen_0_valid_output;
logic agg_read_sched_gen_1_valid_output;
logic [2:0] loops_in2buf_autovec_write_0_mux_sel_out;
logic loops_in2buf_autovec_write_0_restart;
logic loops_in2buf_autovec_write_0_step;
logic [2:0] loops_in2buf_autovec_write_1_mux_sel_out;
logic loops_in2buf_autovec_write_1_restart;
logic loops_in2buf_autovec_write_1_step;
assign agg_read_out = agg_read;
assign loops_in2buf_autovec_write_0_step = agg_read[0];
assign floop_mux_sel[0] = loops_in2buf_autovec_write_0_mux_sel_out;
assign floop_restart[0] = loops_in2buf_autovec_write_0_restart;
assign agg_read[0] = agg_read_sched_gen_0_valid_output;
assign loops_in2buf_autovec_write_1_step = agg_read[1];
assign floop_mux_sel[1] = loops_in2buf_autovec_write_1_mux_sel_out;
assign floop_restart[1] = loops_in2buf_autovec_write_1_restart;
assign agg_read[1] = agg_read_sched_gen_1_valid_output;
for_loop_6_16 #(
  .CONFIG_WIDTH(5'h10),
  .ITERATOR_SUPPORT(4'h6))
loops_in2buf_autovec_write_0 (
  .clk(clk),
  .clk_en(clk_en),
  .dimensionality(loops_in2buf_autovec_write_0_dimensionality),
  .flush(flush),
  .ranges(loops_in2buf_autovec_write_0_ranges),
  .rst_n(rst_n),
  .step(loops_in2buf_autovec_write_0_step),
  .mux_sel_out(loops_in2buf_autovec_write_0_mux_sel_out),
  .restart(loops_in2buf_autovec_write_0_restart)
);

sched_gen_6_16 agg_read_sched_gen_0 (
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .enable(agg_read_sched_gen_0_enable),
  .finished(loops_in2buf_autovec_write_0_restart),
  .flush(flush),
  .mux_sel(loops_in2buf_autovec_write_0_mux_sel_out),
  .rst_n(rst_n),
  .sched_addr_gen_starting_addr(agg_read_sched_gen_0_sched_addr_gen_starting_addr),
  .sched_addr_gen_strides(agg_read_sched_gen_0_sched_addr_gen_strides),
  .valid_output(agg_read_sched_gen_0_valid_output)
);

for_loop_6_16 #(
  .CONFIG_WIDTH(5'h10),
  .ITERATOR_SUPPORT(4'h6))
loops_in2buf_autovec_write_1 (
  .clk(clk),
  .clk_en(clk_en),
  .dimensionality(loops_in2buf_autovec_write_1_dimensionality),
  .flush(flush),
  .ranges(loops_in2buf_autovec_write_1_ranges),
  .rst_n(rst_n),
  .step(loops_in2buf_autovec_write_1_step),
  .mux_sel_out(loops_in2buf_autovec_write_1_mux_sel_out),
  .restart(loops_in2buf_autovec_write_1_restart)
);

sched_gen_6_16 agg_read_sched_gen_1 (
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .enable(agg_read_sched_gen_1_enable),
  .finished(loops_in2buf_autovec_write_1_restart),
  .flush(flush),
  .mux_sel(loops_in2buf_autovec_write_1_mux_sel_out),
  .rst_n(rst_n),
  .sched_addr_gen_starting_addr(agg_read_sched_gen_1_sched_addr_gen_starting_addr),
  .sched_addr_gen_strides(agg_read_sched_gen_1_sched_addr_gen_strides),
  .valid_output(agg_read_sched_gen_1_valid_output)
);

endmodule   // strg_ub_agg_sram_shared

module strg_ub_vec (
  input logic [1:0] accessor_output_top,
  input logic [8:0] addr_to_sram_top,
  input logic [3:0] agg_only_agg_read_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] agg_only_agg_read_addr_gen_0_strides,
  input logic [3:0] agg_only_agg_read_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] agg_only_agg_read_addr_gen_1_strides,
  input logic [3:0] agg_only_agg_write_addr_gen_0_starting_addr,
  input logic [5:0] [3:0] agg_only_agg_write_addr_gen_0_strides,
  input logic [3:0] agg_only_agg_write_addr_gen_1_starting_addr,
  input logic [5:0] [3:0] agg_only_agg_write_addr_gen_1_strides,
  input logic agg_only_agg_write_sched_gen_0_enable,
  input logic [15:0] agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_only_agg_write_sched_gen_0_sched_addr_gen_strides,
  input logic agg_only_agg_write_sched_gen_1_enable,
  input logic [15:0] agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_only_agg_write_sched_gen_1_sched_addr_gen_strides,
  input logic [3:0] agg_only_loops_in2buf_0_dimensionality,
  input logic [5:0] [15:0] agg_only_loops_in2buf_0_ranges,
  input logic [3:0] agg_only_loops_in2buf_1_dimensionality,
  input logic [5:0] [15:0] agg_only_loops_in2buf_1_ranges,
  input logic agg_sram_shared_agg_read_sched_gen_0_enable,
  input logic [15:0] agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides,
  input logic agg_sram_shared_agg_read_sched_gen_1_enable,
  input logic [15:0] agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr,
  input logic [5:0] [15:0] agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides,
  input logic [3:0] agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality,
  input logic [5:0] [15:0] agg_sram_shared_loops_in2buf_autovec_write_0_ranges,
  input logic [3:0] agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality,
  input logic [5:0] [15:0] agg_sram_shared_loops_in2buf_autovec_write_1_ranges,
  input logic cen_to_sram_top,
  input logic clk,
  input logic clk_en,
  input logic [3:0] [15:0] data_from_strg,
  input logic [1:0] [15:0] data_in,
  input logic [1:0] [15:0] data_out_top,
  input logic [3:0] [15:0] data_to_sram_top,
  input logic flush,
  input logic [1:0] [2:0] loops_sram2tb_mux_sel_top,
  input logic [1:0] loops_sram2tb_restart_top,
  input logic rst_n,
  input logic [1:0] t_read_out_top,
  input logic wen_to_sram_top,
  output logic [1:0] accessor_output,
  output logic [8:0] addr_out,
  output logic cen_to_strg,
  output logic [1:0] [15:0] data_out,
  output logic [3:0] [15:0] data_to_strg,
  output logic [1:0][3:0] [15:0] strg_ub_agg_data_out,
  output logic wen_to_strg
);

logic [1:0] agg_only_agg_read;
logic [1:0][2:0] agg_only_floop_mux_sel;
logic [1:0] agg_only_floop_restart;
logic [15:0] cycle_count;

always_ff @(posedge clk, negedge rst_n) begin
  if (~rst_n) begin
    cycle_count <= 16'h0;
  end
  else if (clk_en) begin
    if (flush) begin
      cycle_count <= 16'h0;
    end
    else if (1'h1) begin
      cycle_count <= cycle_count + 16'h1;
    end
  end
end
assign wen_to_strg = wen_to_sram_top;
assign cen_to_strg = cen_to_sram_top;
assign addr_out = addr_to_sram_top;
assign data_to_strg = data_to_sram_top;
assign accessor_output = accessor_output_top;
assign data_out = data_out_top;
strg_ub_agg_only agg_only (
  .agg_read(agg_only_agg_read),
  .agg_read_addr_gen_0_starting_addr(agg_only_agg_read_addr_gen_0_starting_addr),
  .agg_read_addr_gen_0_strides(agg_only_agg_read_addr_gen_0_strides),
  .agg_read_addr_gen_1_starting_addr(agg_only_agg_read_addr_gen_1_starting_addr),
  .agg_read_addr_gen_1_strides(agg_only_agg_read_addr_gen_1_strides),
  .agg_write_addr_gen_0_starting_addr(agg_only_agg_write_addr_gen_0_starting_addr),
  .agg_write_addr_gen_0_strides(agg_only_agg_write_addr_gen_0_strides),
  .agg_write_addr_gen_1_starting_addr(agg_only_agg_write_addr_gen_1_starting_addr),
  .agg_write_addr_gen_1_strides(agg_only_agg_write_addr_gen_1_strides),
  .agg_write_sched_gen_0_enable(agg_only_agg_write_sched_gen_0_enable),
  .agg_write_sched_gen_0_sched_addr_gen_starting_addr(agg_only_agg_write_sched_gen_0_sched_addr_gen_starting_addr),
  .agg_write_sched_gen_0_sched_addr_gen_strides(agg_only_agg_write_sched_gen_0_sched_addr_gen_strides),
  .agg_write_sched_gen_1_enable(agg_only_agg_write_sched_gen_1_enable),
  .agg_write_sched_gen_1_sched_addr_gen_starting_addr(agg_only_agg_write_sched_gen_1_sched_addr_gen_starting_addr),
  .agg_write_sched_gen_1_sched_addr_gen_strides(agg_only_agg_write_sched_gen_1_sched_addr_gen_strides),
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .data_in(data_in),
  .floop_mux_sel(agg_only_floop_mux_sel),
  .floop_restart(agg_only_floop_restart),
  .flush(flush),
  .loops_in2buf_0_dimensionality(agg_only_loops_in2buf_0_dimensionality),
  .loops_in2buf_0_ranges(agg_only_loops_in2buf_0_ranges),
  .loops_in2buf_1_dimensionality(agg_only_loops_in2buf_1_dimensionality),
  .loops_in2buf_1_ranges(agg_only_loops_in2buf_1_ranges),
  .rst_n(rst_n),
  .agg_data_out(strg_ub_agg_data_out)
);

strg_ub_agg_sram_shared agg_sram_shared (
  .agg_read_sched_gen_0_enable(agg_sram_shared_agg_read_sched_gen_0_enable),
  .agg_read_sched_gen_0_sched_addr_gen_starting_addr(agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_starting_addr),
  .agg_read_sched_gen_0_sched_addr_gen_strides(agg_sram_shared_agg_read_sched_gen_0_sched_addr_gen_strides),
  .agg_read_sched_gen_1_enable(agg_sram_shared_agg_read_sched_gen_1_enable),
  .agg_read_sched_gen_1_sched_addr_gen_starting_addr(agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_starting_addr),
  .agg_read_sched_gen_1_sched_addr_gen_strides(agg_sram_shared_agg_read_sched_gen_1_sched_addr_gen_strides),
  .clk(clk),
  .clk_en(clk_en),
  .cycle_count(cycle_count),
  .flush(flush),
  .loops_in2buf_autovec_write_0_dimensionality(agg_sram_shared_loops_in2buf_autovec_write_0_dimensionality),
  .loops_in2buf_autovec_write_0_ranges(agg_sram_shared_loops_in2buf_autovec_write_0_ranges),
  .loops_in2buf_autovec_write_1_dimensionality(agg_sram_shared_loops_in2buf_autovec_write_1_dimensionality),
  .loops_in2buf_autovec_write_1_ranges(agg_sram_shared_loops_in2buf_autovec_write_1_ranges),
  .rst_n(rst_n),
  .agg_read_out(agg_only_agg_read),
  .floop_mux_sel(agg_only_floop_mux_sel),
  .floop_restart(agg_only_floop_restart)
);

endmodule   // strg_ub_vec

