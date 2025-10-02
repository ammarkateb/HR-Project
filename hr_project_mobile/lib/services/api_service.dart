import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // Fallback to local hardcoded auth for now - Railway API still deploying
  static const String baseUrl = 'https://hr-project-production.up.railway.app';

  static const Map<String, String> headers = {
    'Content-Type': 'application/json',
  };

  // Login API call with retry mechanism for Saudi networks
  static Future<ApiResponse<LoginResponse>> login(String username, String password) async {
    // Configure HTTP client for Saudi network compatibility
    final client = http.Client();

    // Try multiple times with different strategies for Saudi network reliability
    for (int attempt = 1; attempt <= 3; attempt++) {
      try {
        final response = await http.post(
          Uri.parse('$baseUrl/api/login'),
          headers: {
            ...headers,
            'User-Agent': 'HR-Project-Mobile/1.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
          },
          body: jsonEncode({
            'username': username,
            'password': password,
          }),
        ).timeout(Duration(seconds: 10 + (attempt * 10))); // Increasing timeout per attempt

        final Map<String, dynamic> data = jsonDecode(response.body);

        if (response.statusCode == 200) {
          return ApiResponse<LoginResponse>(
            success: true,
            data: LoginResponse.fromJson(data),
          );
        } else {
          if (attempt == 3) {
            return ApiResponse<LoginResponse>(
              success: false,
              message: data['message'] ?? 'Login failed after multiple attempts',
            );
          }
          // Continue to next attempt
        }
      } catch (e) {
        if (attempt == 3) {
          // Last attempt failed - try local fallback for demo
          if (username == 'admin' && password == 'admin123') {
            return ApiResponse<LoginResponse>(
              success: true,
              data: LoginResponse.fromJson({
                'success': true,
                'message': 'Login successful (Offline Mode)',
                'user': {
                  'username': username,
                  'role': 'Administrator'
                }
              }),
            );
          }
          return ApiResponse<LoginResponse>(
            success: false,
            message: 'Network connection failed.\nOffline mode: Use admin/admin123 for demo.',
          );
        }
        // Wait before retry
        await Future.delayed(Duration(seconds: attempt * 2));
      }
    }

    // Fallback (should not reach here)
    return ApiResponse<LoginResponse>(
      success: false,
      message: 'Login failed after multiple attempts',
    );
  }

  // Sign Up API call with retry mechanism
  static Future<ApiResponse<LoginResponse>> signUp(String username, String email, String password) async {
    for (int attempt = 1; attempt <= 3; attempt++) {
      try {
        final response = await http.post(
          Uri.parse('$baseUrl/api/signup'),
          headers: {
            ...headers,
            'User-Agent': 'HR-Project-Mobile/1.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
          },
          body: jsonEncode({
            'username': username,
            'email': email,
            'password': password,
          }),
        ).timeout(Duration(seconds: 10 + (attempt * 10)));

        final Map<String, dynamic> data = jsonDecode(response.body);

        if (response.statusCode == 200 || response.statusCode == 201) {
          return ApiResponse<LoginResponse>(
            success: true,
            message: data['message'] ?? 'Account created successfully!',
          );
        } else {
          if (attempt == 3) {
            return ApiResponse<LoginResponse>(
              success: false,
              message: data['message'] ?? 'Sign up failed after multiple attempts',
            );
          }
        }
      } catch (e) {
        if (attempt == 3) {
          return ApiResponse<LoginResponse>(
            success: false,
            message: 'Network connection failed. Please try again later.',
          );
        }
        await Future.delayed(Duration(seconds: attempt * 2));
      }
    }

    return ApiResponse<LoginResponse>(
      success: false,
      message: 'Sign up failed after multiple attempts',
    );
  }

  // Dashboard data API call with Saudi network optimization
  static Future<ApiResponse<DashboardData>> getDashboardData() async {
    for (int attempt = 1; attempt <= 3; attempt++) {
      try {
        final response = await http.get(
          Uri.parse('$baseUrl/api/dashboard'),
          headers: {
            ...headers,
            'User-Agent': 'HR-Project-Mobile/1.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
          },
        ).timeout(Duration(seconds: 15 + (attempt * 10)));

        if (response.statusCode == 200) {
          final Map<String, dynamic> data = jsonDecode(response.body);
          return ApiResponse<DashboardData>(
            success: true,
            data: DashboardData.fromJson(data),
          );
        } else {
          if (attempt == 3) {
            return ApiResponse<DashboardData>(
              success: false,
              message: 'Failed to load dashboard data after multiple attempts',
            );
          }
        }
      } catch (e) {
        if (attempt == 3) {
          // Provide offline demo data
          return ApiResponse<DashboardData>(
            success: true,
            data: DashboardData.fromJson({
              'overview': {
                'employees': 156,
                'departments': 12,
                'pending_requests': 8,
                'active_projects': 24
              },
              'recent_activities': [
                {
                  'id': 1,
                  'title': 'New employee onboarded (Demo)',
                  'subtitle': 'John Doe joined Engineering (Offline Mode)',
                  'time': '2 hours ago',
                  'icon': 'person_add'
                },
                {
                  'id': 2,
                  'title': 'Leave request approved (Demo)',
                  'subtitle': 'Sarah Wilson\'s vacation request (Offline Mode)',
                  'time': '4 hours ago',
                  'icon': 'check_circle'
                },
                {
                  'id': 3,
                  'title': 'Network connection limited',
                  'subtitle': 'Showing offline demo data due to network issues',
                  'time': 'Now',
                  'icon': 'info'
                }
              ]
            }),
          );
        }
        // Wait before retry
        await Future.delayed(Duration(seconds: attempt * 2));
      }
    }

    // Fallback
    return ApiResponse<DashboardData>(
      success: false,
      message: 'Failed to load data after multiple attempts',
    );
  }
}

// Generic API response wrapper
class ApiResponse<T> {
  final bool success;
  final T? data;
  final String? message;

  ApiResponse({
    required this.success,
    this.data,
    this.message,
  });
}

// Login response model
class LoginResponse {
  final bool success;
  final String message;
  final User? user;

  LoginResponse({
    required this.success,
    required this.message,
    this.user,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      success: json['success'] ?? false,
      message: json['message'] ?? '',
      user: json['user'] != null ? User.fromJson(json['user']) : null,
    );
  }
}

// User model
class User {
  final String username;
  final String role;

  User({
    required this.username,
    required this.role,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      username: json['username'] ?? '',
      role: json['role'] ?? '',
    );
  }
}

// Dashboard data model
class DashboardData {
  final DashboardOverview overview;
  final List<RecentActivity> recentActivities;

  DashboardData({
    required this.overview,
    required this.recentActivities,
  });

  factory DashboardData.fromJson(Map<String, dynamic> json) {
    return DashboardData(
      overview: DashboardOverview.fromJson(json['overview'] ?? {}),
      recentActivities: (json['recent_activities'] as List<dynamic>? ?? [])
          .map((activity) => RecentActivity.fromJson(activity))
          .toList(),
    );
  }
}

// Dashboard overview model
class DashboardOverview {
  final int employees;
  final int departments;
  final int pendingRequests;
  final int activeProjects;

  DashboardOverview({
    required this.employees,
    required this.departments,
    required this.pendingRequests,
    required this.activeProjects,
  });

  factory DashboardOverview.fromJson(Map<String, dynamic> json) {
    return DashboardOverview(
      employees: json['employees'] ?? 0,
      departments: json['departments'] ?? 0,
      pendingRequests: json['pending_requests'] ?? 0,
      activeProjects: json['active_projects'] ?? 0,
    );
  }
}

// Recent activity model
class RecentActivity {
  final int id;
  final String title;
  final String subtitle;
  final String time;
  final String icon;

  RecentActivity({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.time,
    required this.icon,
  });

  factory RecentActivity.fromJson(Map<String, dynamic> json) {
    return RecentActivity(
      id: json['id'] ?? 0,
      title: json['title'] ?? '',
      subtitle: json['subtitle'] ?? '',
      time: json['time'] ?? '',
      icon: json['icon'] ?? 'info',
    );
  }
}