#include<cstdio>

char* flags[6] = {
	"answer.flg",  "busy.flg",  
	"ians.flg",  "ireq.flg",  
	"request.flg",  "sensor_data.flg"
};

int main() {
	FILE *f;
	for(int i=0; i<6; i++) {
		f = fopen(flags[i], "w");
		fprintf(f, "7 7 7 7 7 7 7 7");
		fclose(f);
	}
	return 0;
}
