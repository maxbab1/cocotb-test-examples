`timescale 1ns/100ps

// this module is basically a counter for the BCID
// it can either operate in master or slave mode
//   in master mode, it is really just a counter (to enable this, tie BcidIn and Latency to '0)
//   in slave mode, the counter waits after a reset until the BcidIn == CONF_LATENCY and then starts from zero
// Reset is the global chip reset, in our case, this is basically the same as ResetLatency which is intended to be set
//   when the config is updated
module bcid_counter #(
        parameter BCID_WIDTH = 9,
        parameter PRESCALE_BITS = 2
    ) (
        input logic Clk, Reset, ResetLatency,
        input logic [BCID_WIDTH-1:0] BcidIn,  // the current time

        output logic [BCID_WIDTH-1:0] BcidOut,

        input logic [BCID_WIDTH-1:0] CONF_LATENCY,
        input logic [PRESCALE_BITS-1:0] CONF_PRESCALER
    );
    
    logic run;
    logic [PRESCALE_BITS-1:0] prescaler_counter;
    
    always_ff@(posedge Clk)
		if(Reset | ResetLatency) begin
			run <= '0;
			BcidOut <= '0;
            prescaler_counter <= '0;
        end else begin
            prescaler_counter <= prescaler_counter + 1'b1;
            if (prescaler_counter == CONF_PRESCALER) begin
                prescaler_counter <= 0;

                if(run)
                    BcidOut <= BcidOut + 1'b1;
                else if (BcidIn == CONF_LATENCY) begin
                    run <= 1;
                    BcidOut <= BcidOut + 1'b1;
                end
            end
        end


    `ifndef SYNTH
        `ifndef VERILATOR
            initial begin
                $dumpfile("dump.vcd");
                $dumpvars(6, bcid_counter);
            end
        `endif
    `endif
endmodule

