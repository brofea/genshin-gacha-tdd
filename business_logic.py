def calculate_gacha_probability(pull_num):
	"""计算指定抽数下的五星概率。"""
	if pull_num <= 0:
		raise ValueError("pull_num must be a positive integer")

	# 超过 90 抽后重置到新一轮（1-90）
	normalized_pull = ((pull_num - 1) % 90) + 1

	if normalized_pull <= 73:
		return 0.006
	if normalized_pull <= 89:
		probability = 0.066
		for _ in range(74, normalized_pull):
			probability += 0.06
		return probability
	return 1.0
