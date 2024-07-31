## Frontend

```
cd frontend
```


### Run

Debug mode:
```
flutter run --web-renderer html -d chrome
```

Release mode:
```
flutter run --web-renderer html --release -d chrome
```

### Build

```
flutter build web --web-renderer html --release
```

### Deploy

```
firebase deploy
```

## Backend

```
cd backend
```

```
npm run build
firebase emulators:start
firebase deploy --only functions
firebase login --reauth
```
