# DevSecOps Project 6 - Gamified Office Management System

### Team Members:
- Gilad Iosef
- Max Zalmanov

## 🎮 Overview
Transform boring office tasks into exciting games! Create competitions for everything - code quality, energy saving, fitness, learning, team challenges. Complete with leaderboards, achievements, and rewards!

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the project
git clone https://github.com/Gidiy/DevSecOps-Project6.git
cd DevSecOps-Project6

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Run the application
python main.py

# Stop the application
Ctrl + C

# Deactivate virtual environment
deactivate
```

## 🏗️ Project Structure
```
DevSecOps-Project6/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (exposed for temporary use)
├── classes/
│   └── user.py           # User model
├── routes/
│   ├── login.py          # Authentication routes
│   ├── games.py          # Game competitions
│   ├── achievements.py   # Achievement system
│   ├── leaderboards.py   # Leaderboard management
│   ├── social.py         # Social features
│   ├── rewards.py        # Reward system
│   └── competitions.py   # Competition categories
├── templates/
│   └── homepage.html     # Main UI interface
├── static/
│   └── presets.txt       # API request presets
└── utils/
    ├── db.py            # Database configuration
    ├── utils.py         # Utility functions
    └── logger.py        # Logging system
```

## 🎯 Features

### 🏆 Achievement System
- **Rarity-based Points**: Common (10), Rare (20), Epic (40), Legendary (80)
- **User-specific**: Achievements are tied to individual accounts
- **Custom Creation**: Create custom achievements with descriptions
- **Unlock/Lock**: Admin controls for achievement management

### 🏅 Leaderboards
- **Global Leaderboard**: Overall office rankings
- **Team Leaderboard**: Team-specific rankings (only team members)
- **Monthly Leaderboard**: Monthly performance tracking
- **Hall of Fame**: All-time top performers
- **Predictions**: Submit and view winner predictions
- **Manual Entries**: Add/edit points for users
- **Real-time Updates**: Automatic refresh after changes

### 🎮 Game System
- **Custom Competitions**: Create your own games
- **Join/Leave**: Easy participation management
- **Progress Tracking**: Update scores and track progress
- **Active Games**: View all ongoing competitions
- **Duration Display**: Start/end dates in readable format

### 👥 Social Features
- **Team Creation**: Form teams with multiple members
- **Activity Feed**: Track team creation and challenges
- **Challenges**: Send personal challenges to colleagues
- **Rivalries**: View ongoing office rivalries
- **Celebrations**: Automatic achievement celebrations

### 🎁 Reward System
- **Point-based**: Earn points from achievements and games
- **Redeem Rewards**: Use points to purchase rewards
- **Donation System**: Transfer points between users
- **Available Rewards**: Browse and manage reward catalog
- **Point Tracking**: Real-time point balance updates

## 🔧 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login

### Games & Competitions
- `GET /games/active` - View active competitions
- `POST /games/create` - Create new competition
- `POST /games/join` - Join a competition
- `PUT /games/progress/update` - Update competition progress
- `DELETE /games/competition/remove` - Remove competition
- `DELETE /games/participation/remove` - Remove participation

### Achievements
- `GET /achievements/available` - View available achievements
- `POST /achievements/unlock` - Unlock achievement
- `POST /achievements/lock` - Lock achievement
- `POST /achievements/create-custom` - Create custom achievement
- `DELETE /achievements/achievement/remove` - Remove achievement
- `DELETE /achievements/user-achievement/remove` - Remove user achievement

### Leaderboards
- `GET /leaderboards/global` - Global leaderboard
- `GET /leaderboards/team` - Team leaderboard
- `GET /leaderboards/monthly` - Monthly leaderboard
- `GET /leaderboards/hall-of-fame` - Hall of fame
- `POST /leaderboards/add` - Add manual entry
- `DELETE /leaderboards/remove` - Remove entry
- `GET /leaderboards/predictions` - View predictions
- `POST /leaderboards/predictions` - Submit prediction
- `DELETE /leaderboards/predictions/remove` - Remove prediction

### Social Features
- `POST /social/teams/create` - Create team
- `GET /social/activity-feed` - View activity feed
- `POST /social/challenges/send` - Send challenge
- `GET /social/challenges/view` - View challenges
- `GET /social/rivalries` - View rivalries
- `GET /social/celebrations` - View celebrations
- `DELETE /social/activity/remove` - Remove activity
- `DELETE /social/challenges/remove` - Remove challenge

### Rewards
- `GET /rewards/available` - View available rewards
- `POST /rewards/add` - Add new reward
- `POST /rewards/redeem` - Redeem reward
- `POST /rewards/donate-points` - Donate points to user
- `DELETE /rewards/remove` - Remove reward

### Competition Categories
- `POST /competitions/code-quality` - Code quality competitions
- `POST /competitions/learning` - Learning challenges
- `POST /competitions/fitness` - Office fitness challenges
- `POST /competitions/sustainability` - Green office competitions
- `POST /competitions/creativity` - Creative challenges
- `POST /competitions/team-building` - Team building activities

## 🎨 User Interface
- **Modern Design**: Clean, responsive interface with dark theme
- **Interactive Tables**: Sortable, filterable data tables
- **Real-time Updates**: Automatic refresh after operations
- **Action Buttons**: Join, Remove, Unlock, Redeem, etc.
- **Modal Forms**: Easy data entry with validation
- **Progress Tracking**: Visual progress indicators

## 🗄️ Database Models

### Core Models
- **User**: User accounts and authentication
- **Competition**: Game competitions
- **Participation**: User participation in competitions (from games route)
- **UserCompetition**: User participation in competitions (from competitions route)
- **Game**: Custom game rules

### Achievement System
- **Achievement**: Achievement definitions with rarity
- **UserAchievement**: User-specific achievement unlocks
- **Celebration**: Achievement celebration records

### Social System
- **UserTeam**: Team membership tracking
- **SocialActivity**: Activity feed entries
- **Challenge**: Personal challenges between users

### Reward System
- **Reward**: Available rewards catalog
- **Redemption**: User reward redemptions

### Leaderboard System
- **ManualLeaderboard**: Legacy manual entries
- **ManualLeaderboardEntry**: Board-specific manual entries
- **Prediction**: Winner predictions

## 🔐 Security Features
- **JWT Authentication**: Secure token-based authentication
- **User Validation**: Input validation and sanitization
- **Optional Authentication**: Anonymous access where appropriate
- **CORS Support**: Cross-origin request handling

## 🚀 Deployment
The application runs on `http://127.0.0.1:5001` by default.

### Environment Variables
- `SECRET_KEY`: JWT secret key (defaults to 'dev-secret-change-me')
- `DATABASE_URL`: Database connection string

## 📝 Development Notes
- **Database**: SQLite with automatic table creation
- **Logging**: Comprehensive request/response logging
- **Error Handling**: Graceful error handling with user feedback
- **Code Organization**: Modular structure with blueprints
- **Frontend**: Vanilla JavaScript with Tailwind CSS

## 🎯 Team Assignment
- **Student 1**: Game engine and achievement system
- **Student 2**: Competition management and social features  
- **Student 3**: Leaderboards and reward system

## 🔄 Recent Updates
- ✅ **Donation System**: User-to-user point transfers
- ✅ **Team Management**: Team creation and membership tracking
- ✅ **Activity Feed**: Real-time social activity tracking
- ✅ **Achievement Rarity**: Point-based achievement system
- ✅ **Clean UI**: Modern table displays with action buttons
- ✅ **Real-time Updates**: Automatic refresh after operations
- ✅ **Prediction System**: Winner prediction functionality
- ✅ **Celebration System**: Automatic achievement celebrations
- ✅ **Dual Competition System**: Separate tracking for games route vs competitions route participation
- ✅ **UserCompetition Model**: New database model for competitions route participation tracking

## 🐛 Troubleshooting
- **Database Issues**: Delete `instance/games.db` to reset database
- **Import Errors**: Ensure all dependencies are installed
- **Port Conflicts**: Change port in `main.py` if 5001 is occupied
- **Authentication**: Check JWT token validity for protected routes

## 📞 Support
For issues or questions, please check the server logs for detailed error messages.
