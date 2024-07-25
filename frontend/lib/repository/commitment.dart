import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:intl/intl.dart';

import '../models/commitment.dart';

final commitmentRepositoryProvider = Provider((ref) => CommitmentRepository());

class CommitmentRepository {
  final _ref = FirebaseFirestore.instance.collection("commitments");

  Future<List<Commitment>?> getCommitment(DateTime date) async {
    final dateString = DateFormat("yyyy-MM-dd").format(date);

    final doc = await _ref.doc(dateString).get();
    if (!doc.exists) {
      return null;
    }
    final dataMap = doc.data() as Map<String, dynamic>;

    List<Commitment> commitments = [];
    dataMap.forEach((userId, data) {
      if (data["enabled"]) {
        commitments.add(Commitment(
          date: date,
          userId: userId,
          userName: data["userName"],
          time: data["time"],
        ));
      }
    });

    return commitments;
  }

  Future<UserCommitment?> getUserCommitment(
      String userId, List<DateTime> dates) async {
    List<Commitment> userCommits = [];

    for (final date in dates) {
      final commits = await getCommitment(date);
      if (commits == null) {
        continue;
      }

      for (final commit in commits!) {
        if (commit.userId == userId) {
          userCommits.add(commit);
        }
      }
    }

    if (userCommits.isEmpty) {
      return null;
    }

    final userCommitment = UserCommitment(
      userId: userId,
      userName: userCommits.first.userName,
      time: userCommits.first.time,
      dates: userCommits.map((commit) => commit.date!).toList(),
    );

    print("Get user commitment: $userCommitment");

    return userCommitment;
  }
}
