#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ROWS 10
#define COLS 10
#define RED_TEXT "\033[1;31m"
#define GREEN_TEXT "\033[1;32m"
#define YELLOW_TEXT "\033[1;33m"
#define BLUE_TEXT "\033[1;34m"
#define MAGENTA_TEXT "\033[1;35m"
#define CYAN_TEXT "\033[1;36m"
#define WHITE_TEXT "\033[1;37m"
#define VIOLET_TEXT "\033[38;5;92m"   

#define RED_BG "\033[41m"
#define GREEN_BG "\033[42m"
#define YELLOW_BG "\033[43m"
#define BLUE_BG "\033[44m"
#define MAGENTA_BG "\033[45m"
#define CYAN_BG "\033[46m"
#define WHITE_BG "\033[47m"
#define VIOLET_BG "\033[48;5;92m"
#define GREY_BG "\033[100m"

#define RESET "\033[0m"

typedef struct {
    char title[50];
    char language[20];
    int availableSeats;
    int price_front;
    int price_middle;
    int price_back;
    char seats[ROWS][COLS];
} Movie;

void initialize_seats(Movie *movie) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            movie->seats[i][j] = '*'; 
        }
    }
}

void display_seats(Movie *movie) {
    printf("\n      " RED_BG" SCREEN "RESET"        \n");
    printf("\n");

    for (int i = 0; i < ROWS; i++) {
        printf(" "); 
        for (int j = 0; j < COLS; j++) {
            if (movie->seats[i][j] == '*') {  
                printf("\033[1;32;100m%c \033[0m", movie->seats[i][j]);
            } else {  
                printf("\033[1;31m%c \033[0m", movie->seats[i][j]);
            }
        }
        printf("\n");  
    }    
    printf("\n");
}

void save_ticket_to_file(char *user_name, char *movie_name, int seats_booked[][2], int num_seats, int total_cost) {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    char filename[100];
    snprintf(filename, sizeof(filename), "ticket_%d-%02d-%02d_%02d-%02d-%02d.txt", 
             tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);

    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error creating ticket file");
        return;
    }

    fprintf(file, "--------------------------------------\n");
    fprintf(file, "          Movie Ticket Receipt        \n");
    fprintf(file, "--------------------------------------\n\n");
    fprintf(file, "User Name: %s\n", user_name);
    fprintf(file, "Movie Name: %s\n\n", movie_name);
    fprintf(file, "Seats Booked:\n");
    for (int i = 0; i < num_seats; i++) {
        fprintf(file, "  - Row %d, Seat %d\n", seats_booked[i][0] + 1, seats_booked[i][1] + 1);
    }
    fprintf(file, "\nTotal Cost: Rs. %d\n\n", total_cost);
    fprintf(file, "Thank you for booking with us!\n");
    fprintf(file, "--------------------------------------\n");

    fclose(file);
    printf("\nTicket has been saved to '%s'.\n", filename);
}

void book_seats(Movie *movie, char *user_name) {
    int seats, row, col, s;
    int total_cost = 0;
    int booked_seats[100][2]; 

    printf("\nSeats Available: %d\n", movie->availableSeats);
    display_seats(movie);

    printf("%s, Enter the number of seats you want to book: ", user_name);
    while (scanf("%d", &seats) != 1 || seats <= 0 || seats > movie->availableSeats) {
        printf("Invalid number of seats. Please enter again: ");
        while (getchar() != '\n');
    }

    printf(YELLOW_TEXT"Select seat section : "RESET"\n1) Front (Rs. %d)\n2) Center (Rs. %d)\n3) Back (Rs. %d)\n" GREEN_TEXT"Enter your choice: "RESET, movie->price_front, movie->price_middle, movie->price_back);
    while (scanf("%d", &s) != 1 || s < 1 || s > 3) {
        printf("Invalid section selection. Please enter again: ");
        while (getchar() != '\n'); 
    }

    for (int i = 0; i < seats; i++) {
        printf("Enter row (%d-%d) and column (1-10) for seat %d: ",(s==1?1:s==2?4:8),(s==1?3:s==2?7:10), i + 1);
        while (scanf("%d %d", &row, &col) != 2 ||
               row < 1 || row > ROWS ||
               col < 1 || col > COLS ||
               movie->seats[row - 1][col - 1] == 'X' ||
               (s == 1 && (row < 1 || row > 3)) ||      
               (s == 2 && (row < 4 || row > 7)) ||     
               (s == 3 && (row < 8 || row > 10))) {
            printf("Invalid or already booked seat. Please enter a valid seat in the selected section: ");
            while (getchar() != '\n'); 
        }

        movie->seats[row - 1][col - 1] = 'X';
        booked_seats[i][0] = row - 1;
        booked_seats[i][1] = col - 1;

        switch (s) {
            case 1:
                total_cost += movie->price_front;
                break;
            case 2:
                total_cost += movie->price_middle;
                break;
            case 3:
                total_cost += movie->price_back;
                break;
        }
    }

    printf("\nTotal cost: Rs. %d\n", total_cost);
    printf(GREEN_TEXT"Confirm booking?" RESET " (1 for Yes, 0 for No): ");
    int confirm;
    while (scanf("%d", &confirm) != 1 || confirm < 0 || confirm > 1) {
        printf("Invalid input. Please enter 1 for Yes or 0 for No: ");
        while (getchar() != '\n'); 
    }

    if (confirm != 1) {
        printf("Booking canceled.\n");
        return;
    }

    printf("\nSelect payment method:\n1) Credit Card\n2) Debit Card\n3) Cash\n" GREEN_TEXT"Enter your choice: " RESET);
    int payment_method;
    while (scanf("%d", &payment_method) != 1 || payment_method < 1 || payment_method > 3) {
        printf("Invalid payment method. Please enter again: ");
        while (getchar() != '\n'); 
    }

    movie->availableSeats -= seats;
    printf("Booking confirmed! %d seats booked for %s.\n", seats, movie->title);
    save_ticket_to_file(user_name, movie->title, booked_seats, seats, total_cost);

    printf("\nWould you like to book another ticket? (1 for Yes, 0 for No): ");
    while (scanf("%d", &confirm) != 1 || confirm < 0 || confirm > 1) {
        printf("Invalid input. Please enter 1 for Yes or 0 for No: ");
        while (getchar() != '\n'); 
    }

    if (confirm == 1) {
        return;
    } else {
        printf("Exiting... Thank you for using the movie booking system!\n");
        exit(0); 
    }
}

int select_movie(Movie movies[], int count) {
    printf(YELLOW_TEXT"\nMovies Available:\n" RESET);
    for (int i = 0; i < count; i++) {
        printf("%d) %s (Available: %d)\n", i + 1, movies[i].title, movies[i].availableSeats);
    }
    printf(GREEN_TEXT"Enter your choice: "RESET);
    int choice;
    while (scanf("%d", &choice) != 1 || choice < 1 || choice > count) {
        printf("Invalid movie choice. Please enter again: ");
        while (getchar() != '\n'); 
    }

    return choice - 1;
}

int main() {
    printf("TTTTT  I  CCCCC  K   K  EEEEE  TTTTT      BBBB   OOOOO  OOOOO  K   K  III  N   N  GGGGG\n");
    printf("  T    I  C      K  K   E        T        B   B  O   O  O   O  K  K    I   NN  N  G    \n");
    printf("  T    I  C      KKK    EEEE     T        BBBB   O   O  O   O  KKK     I   N N N  G  GG\n");
    printf("  T    I  C      K  K   E        T        B   B  O   O  O   O  K  K    I   N  NN  G   G\n");
    printf("  T    I  CCCCC  K   K  EEEEE    T        BBBB   OOOOO  OOOOO  K   K  III  N   N   GGGG\n");

    printf("\n");
    char user_name[50];
    printf(YELLOW_TEXT"Enter your name : "RESET);
    scanf(" %49s", user_name);

    Movie movies[] = {
        {"Marco", "English", 50, 250, 200, 150, {}},
        {"Avengers: Endgame", "English", 30, 300, 250, 200, {}},
        {"Avatar", "English", 40, 350, 300, 250, {}},
        {"Spider-Man: No Way Home", "English", 35, 320, 280, 240, {}},
        {"Jurassic Park", "English", 45, 280, 240, 200, {}},
        {"Gadar 2", "Hindi", 50, 220, 180, 140, {}},
        {"Pushpa 2", "Hindi", 40, 270, 230, 190, {}},
        {"Jawan", "Hindi", 30, 300, 250, 200, {}},
        {"3 Idiots", "Hindi", 45, 250, 200, 150, {}},
        {"Bhool Bhulaiyaa 2", "Hindi", 35, 280, 230, 180, {}},
        {"Lai Bhaari", "Marathi", 50, 200, 160, 120, {}},
        {"Sairat", "Marathi", 40, 220, 180, 140, {}},
        {"Natsamrat", "Marathi", 30, 250, 200, 150, {}},
        {"Timepass", "Marathi", 45, 230, 190, 150, {}},
        {"Duniyadari", "Marathi", 35, 240, 200, 160, {}},
    };
    int movieCount = sizeof(movies) / sizeof(movies[0]);

    for (int i = 0; i < movieCount; i++) {
        initialize_seats(&movies[i]);
    }

    while (1) {
        printf(YELLOW_TEXT"\nSelect Movie Language : " RESET
            BLUE_TEXT"\n1) English  "RESET
            VIOLET_TEXT"\n2) Hindi    "RESET
            MAGENTA_TEXT"\n3) Marathi  "RESET
            RED_TEXT"\n4) Exit     "RESET
            GREEN_TEXT"\nEnter your choice: "RESET);
        int choice;
        while (scanf("%d", &choice) != 1 || choice < 1 || choice > 4) {
            printf("Invalid selection. Please enter again: ");
            while (getchar() != '\n');
        }

        Movie *selected_movies;
        int movie_index;

        switch (choice) {
            case 1:
                selected_movies = movies;
                break;
            case 2:
                selected_movies = &movies[5];
                break;
            case 3:
                selected_movies = &movies[10];
                break;
            case 4:
                printf("Exiting... Thank you for using the movie booking system!\n");
                return 0;
        }

        movie_index = select_movie(selected_movies, 5);
        if (movie_index == -1) {
            continue;
        }

        book_seats(&selected_movies[movie_index], user_name);
    }

    return 0;
}