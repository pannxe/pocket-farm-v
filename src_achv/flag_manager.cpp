#include <cstdio>
#include <chrono>
#include <thread>

#include "common_flags.h"
#include "Flag.cpp"

using namespace std::this_thread; // sleep_for, sleep_until
using namespace std::chrono; // nanoseconds, system_clock, seconds

const int self_id = FLAG;

bool get_sensor() {
    Flag    ir_flag("ireq.flg", "w"),
            ia_flag("ians.flg", "r");
    printf("\n    Request has sent to Sensor Reader Module ");
    ir_flag.set_stat(self_id, REQUESTED);
    ir_flag.refreash("ireq.flg", "w");

    while(true) {
        printf(".");
        ir_flag.refreash("ireq.flg", "w");
        ir_flag.set_stat(self_id, REQUESTED);
        ia_flag.refreash("ians.flg", "r");
        ia_flag.get_data();
        if(ia_flag.is_answered()) {
            ir_flag.set_stat(self_id, ACQUIRED);
            printf("answer acquired\n");
            return true;
        }
        ia_flag.del();
        ir_flag.del();
        sleep_until(system_clock::now() + seconds(3));
    }
    return false;
}

int main() {
    printf("Pocket Farm's\nFLAG MANAGER MODULE\nVERSION 1.0.0\n_________________________\n");
    bool first = false;
    printf("Waiting for request...\n");
    Flag    r_flag ("request.flg", "r"),
            a_flag ("answer.flg", "w+"), 
            b_flag ("busy.flg", "w");

    while(true) {
        r_flag.refreash("request.flg", "r");
        a_flag.refreash("answer.flg", "w+");
        b_flag.refreash("busy.flg", "w");
        
        b_flag.set_stat(self_id, READY);
        r_flag.get_data();
        if (r_flag.is_requested()) {
            first = true;
            b_flag.set_stat(self_id, BUSY);
            int id = r_flag.get_requestor_id();
            printf("Got request from %s\n  --> Processing... ", _cmp[id]);
            if(get_sensor()) {
                a_flag.set_stat(self_id, ANSWERED, id);
                printf("done\n\n");
            }
            else {
                printf("Error!");
                return 1;
            }
        }
        if (r_flag.is_acquired() && first) {
            first = false;
            printf("acquired\n\n");
        }
        //
        r_flag.del();
        a_flag.del();
        b_flag.del();
        sleep_until(system_clock::now() + seconds(1));
    }

    return 0;
}
