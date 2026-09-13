import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_ROOT, "translations", "06_Quests_Events_Story.json")

# Dictionary for Phase 6A (Indices 0 to 334, 335 items)
T_6A = {
  # 1. Tech Tiers & Categories (15 items)
  "tier.1": "Nghiên Cứu Cấp 1",
  "tier.2": "Nghiên Cứu Cấp 2",
  "tier.3": "Nghiên Cứu Cấp 3",
  "tier.4": "Nghiên Cứu Cấp 4",
  "tier.description": "Trang thiết bị tối tân cho phép nghiên cứu các công nghệ phức tạp hơn.",
  "techCategory.housing": "Nhà Ở & Dịch Vụ",
  "techCategory.transport": "Di Chuyển",
  "techCategory.Production": "Sản Xuất",
  "techCategory.Services": "Dịch Vụ",
  "techCategory.Logistics": "Hậu Cần & Băng Tải",
  "techCategory.Beauty": "Cảnh Quan Làm Đẹp",
  "techCategory.Utilities": "Tiện Ích & Băng Chuyền",
  "techCategory.foodProduction": "Lương Thực",
  "techCategory.Science": "Khoa Học",
  "techCategory.naval": "Hàng Hải",

  # 2. UI, Navigation, Controls & Choices (35 items)
  "industrydetail.neareststockpile": "Kho Bãi Gần Nhất",
  "choice.save": "Lưu",
  "choice.cancel": "Hủy",
  "choice.accept": "Chấp Thuận",
  "choice.accepted": "Đã Chấp Thuận",
  "choice.close": "Đóng",
  "choice.refuse": "Từ Chối",
  "choice.acceptQuest": "Nhận Nhiệm Vụ",
  "choice.promisehousing": "Hứa sẽ xây nhà ở",
  "choice.promiseresearch": "Hỗ Trợ Nghiên Cứu",
  "choice.turnInQuest": "Báo Cáo Hoàn Thành",
  "choice.unloadShipment": "Dỡ Kiện Hàng",
  "housingslot.unassigned": "Giường Trống",
  "villager.name": "Chuột Dân",
  "mapgen.mediumsize": "Đảo Vừa",
  "mapgen.largesize": "Đảo Khổng Lồ",
  "policyview.title": "Bảng Quản Lý Chính Sách",
  "agentdetails.nojob": "Chưa Phân Công Việc",
  "agentdetails.nohome": "Giường trống bất kỳ",
  "controller.xbox": "Xbox",
  "controller.playstation": "PlayStation",
  "quality.low": "Kém",
  "quality.standard": "Trung Bình",
  "quality.better": "Tốt",
  "quality.supreme": "Thượng Hạng",
  "toggle.enabled": "Bật",
  "toggle.disabled": "Tắt",
  "cursor.startDrag": "Bắt Đầu Kéo",
  "cursor.holdToBulldoze": "Giữ Để Phá Dỡ",
  "choiceresult.startsquest": "Bắt Đầu Nhiệm Vụ",
  "filter.all": "Tất Cả",
  "filter.nojob": "Chưa Có Việc",
  "filter.nohouse": "Chưa Có Nhà",
  "time.endsTonight": "Kết Thúc Đêm Nay",
  "info.producedIn": "Sản xuất tại:",
  "info.modifier": "Hiệu Ứng Bổ Trợ",

  # Subcategories
  "subcat.basic": "Vật Liệu Thô",
  "subcat.refined": "Vật Liệu Tinh Chế",
  "subcat.raw": "Nguyên Liệu Thô",
  "subcat.ore": "Quặng Khoáng Sản",
  "subcat.rare": "Quý Hiếm",
  "subcat.preparedFood": "Món Đã Chế Biến",
  "subcat.additive": "Phụ Gia",
  "subcat.science": "Khoa Học",
  "subcat.tools": "Dụng Cụ & Tiếp Tế",
  "subcat.tea": "Trà",
  "subcat.rawFood": "Thực Phẩm Thô",
  "subcat.trade": "Hàng Hóa Xuất Khẩu",

  # 3. Tutorial Steps & Initial Guidelines (4 items)
  "tutorialStep.placeDock": "Hãy xây Bến Cảng Chính dọc theo bờ biển.",
  "tutorialStep.acceptArrivals": "Đón bà con chuột tại bến cảng ngay khi tàu cập bến.",
  "tutorialStep.buildWarehouse": "Xây một KHO BÃI gần bến cảng. Bầy chuột sẽ bắt tay vào thi công ngay.",
  "tutorialStep.acceptSupplies": "Dỡ kiện hàng TIẾP TẾ tại bến cảng ngay khi tàu cập bến.",

  # 4. Debt, Taxes & Royal Finances (35 items)
  "debt.populationTax": "Thuế Đầu Chuột",
  "debt.supplyShipment": "Kiện Hàng Tiếp Tế",
  "debt.initialSupplyShipment": "Hàng Tiếp Tế Ban Đầu",
  "debt.newPopulationTax": "Tăng Thuế Đầu Chuột",
  "debt.travelcost_colonists": "Phí vận chuyển tàu chở chuột",
  "debt.travelcost_supplies": "Phí vận chuyển tàu tiếp tế",
  "fee.supplyshipminimumFee": "Phí hải trình (Dỡ thêm hàng tiếp tế)",
  "debt.missedPayments": "Nợ Thuế Tồn Đọng Đợt Trước",
  "debt.productiontax": "Thuế Sản Xuất Công Nghiệp",
  "debt.credit": "Tín Dụng Nhiệm Vụ",
  "debt.policycredit": "Tín Dụng Chính Sách",
  "debt.extraWhiskers": "Chi Phí Cử Thêm Chuột",
  "debt.tax": "Thuế & Nợ Nần",
  "debt.inventory": "Kho Tổng",
  "debt.inventorydesc": "Nộp thuế bằng cách bốc tài nguyên từ kho lên tàu thu thuế của Hoàng Triều.",
  "debt.insufficientpayment": "Chưa Đủ Thuế",
  "debt.sendingpartial": "Đang Gửi Một Phần Thuế",
  "debt.sendingfull": "Đang Gửi Đủ Thuế",
  "debt.sendingbonus": "Đang Nộp Vượt Mức Thuế",
  "debt.sendship": "Cho Tàu Xuất Bến",
  "debt.sendpartial": "Gửi Một Phần Thuế",
  "debt.sendfull": "Gửi Đủ Thuế",
  "debt.sendbonus": "Nộp Vượt Mức Thuế",
  "debt.morerequired": "Cần thêm hàng hóa",
  "debt.upcoming": "Các Đợt Thuế Sắp Tới",
  "debt.basetax": "Thuế Quản Lý Hành Chính",
  "debt.availableExports": "Hàng Xuất Khẩu Khả Dụng",
  "debt.gift.unlock": "Bản Vẽ Kỹ Thuật",
  "debt.gift.effect": "Hiệu Ứng",
  "debt.gift.other": "Khác",
  "titlebar.clawsView": "Báo Cáo Thuế",
  "value.tax.highDemand": "Nhu Cầu Cao",
  "value.tax.noValue": "Không Có Giá Trị Thuế",
  "value.tax.due": "Hạn Nộp",
  "value.tax.storage": "Lưu Trữ",
  "value.tax.shiparriveTime": "Tàu Thu Thuế đến sau <0> Ngày",
  "value.tax.shiparriveTomorrow": "Tàu Thu Thuế đến vào Ngày Mai",
  "value.tax.shiparriveToday": "Tàu Thu Thuế cập bến Hôm Nay!",

  # 5. Approval & Citizen Mood System (15 items)
  "approval.posThought": "Cảm Xúc Tích Cực",
  "approval.negThought": "Cảm Xúc Tiêu Cực",
  "approval.other": "Hành Động Khác",
  "approval.policy.positive": "Lợi Ích Từ Chính Sách",
  "approval.policy.negative": "Tổn Thất Do Chính Sách",
  "approval.reward": "Thưởng Nhiệm Vụ",
  "approval.capacityHint": "Hạn mức Lòng Dân tăng theo quy mô dân số.",
  "approval.estimate": "Dự Tính Lòng Dân Đêm Nay",
  "approval.earned": "Lòng Dân Nhận Được",
  "approval.low": "Bà con chuột bắt đầu hoài nghi tài lãnh đạo của bạn...",
  "approval.max": "Tối Đa",

  # 6. Deaths, Phases & Loading (15 items)
  "death.starvation": "Chết Đói",
  "death.illness": "Bệnh Tật",
  "death.injury": "Chấn Thương",
  "phase.workhours": "Giờ Làm Việc",
  "phase.nighthours": "Buổi Tối",
  "loading.loading": "ĐANG TẢI",
  "loading.mastersync": "Đang đồng bộ dữ liệu Master",
  "loading.initsim": "Đang khởi tạo mô phỏng",
  "loading.loadingsave": "Đang tải bản lưu",
  "loading.almostdone": "Sắp xong rồi!",
  "dialog.collapsed": "đã Sụp Đổ",
  "dialog.lose": "Phe Móng Vuốt chẳng bao lâu sau đã cập bến một hải cảng hoang tàn không bóng chuột.\n\nMột toán lính trinh sát được phái đi lùng sục, nhưng không tìm thấy bất kỳ dấu vết sự sống nào.\n\nThật đáng tiếc...",
  "stat.daysSurvived": "Số ngày sinh tồn",
  "stat.taxesPaid": "Tổng thuế cống nạp đã nộp",

  # 7. Building & Object Tags (30 items)
  "tag.hardlabor": "Lao Động Nặng Nhọc",
  "tag.haswaterAdapter": "Đầu Nối Ống Nước",
  "tag.hasSteamAdapter": "Đầu Nối Ống Hơi Nước",
  "tag.slowTravelSpeed": "Tốc Độ Di Chuyển Chậm",
  "tag.mediumTravelSpeed": "Tốc Độ Di Chuyển Trung Bình",
  "tag.fastTravelSpeed": "Tốc Độ Di Chuyển Nhanh",
  "tag.extremeTravelSpeed": "Tốc Độ Di Chuyển Cực Nhanh",
  "tag.stackable": "Có Thể Xếp Chồng Tầng",
  "tag.heatsource": "Nguồn Tỏa Nhiệt",
  "tag.approvalsource": "Nguồn Tạo Lòng Dân",
  "tag.requiresFiretender": "Cần Thợ Chăm Lửa",
  "tag.nightservice": "Phục Vụ Ban Đêm",
  "tag.decorative": "Được chuột đi ngang qua yêu thích",
  "tag.intimidating": "Uy hiếp chuột đi ngang qua",
  "tag.requiresSea": "Cần Không Gian Biển Thoáng",
  "desc.pathsidedecor": "Đồ trang trí ven lối đi.",
  "tag.automation": "Băng Chuyền Tài Nguyên",
  "tag.guildtrait.extracarry": "+1 sức khuân vác",
  "tag.guildtrait.extraeat": "+1 phần ăn mỗi bữa",
  "tag.guildtrait.reducedwear": "Máy móc công nghiệp ít hao mòn hơn",
  "tag.guildtrait.dislikeraw": "Cực kỳ ghét đồ ăn sống",
  "tag.guildtrait.insulated": "Kháng lạnh tự nhiên",
  "tag.guildtrait.hiker": "Không bị địa hình cản bước",
  "tag.guildtrait.common": "+50% sản lượng trong các xưởng bang hội",
  "tag.researchStorage": "Tăng sức chứa điểm tri thức",
  "tag.customizable": "Có Thể Tùy Biến",
  "tag.temporary": "Tuổi thọ có hạn",
  "tag.storage_large": "Sức chứa kho bãi lớn",
  "tag.storage_small": "Sức chứa kho bãi nhỏ",

  # Counters & Farm Tools
  "counter.researcharchives": "Kho Lưu Trữ Nghiên Cứu",
  "counter.researchLabs": "Phòng Nghiên Cứu Kỹ Nghệ",
  "counter.totalResearch": "Tổng Điểm Tri Thức Đã Đạt",
  "research.missingPrerequsite": "Thiếu Điều Kiện Tiên Quyết",
  "farmtool.newfield": "Ruộng Mới",
  "farmtool.extendField": "Mở Rộng Ruộng",
  "farmtool.shrinkfield": "Thu Hẹp Ruộng",
  "farmtool.configure": "Cấu Hình",
  "vehicle.coastingWagon": "Xe Đẩy Trượt Băng Tải",
  "counter.offices": "Văn Phòng Đã Xây",
  "day.today": "Hôm Nay",
  "day.tomorrow": "Ngày Mai",
  "day.daysAway": "ngày nữa",
  "day.day": "Ngày",
  "day.daysUntil": "ngày cho tới",

  # 8. Story Dialogues & Core Quests (Part 1 - 25 items)
  "story.common.intro1": "Gửi Quyền Trưởng Làng,",
  "story.common.intro2": "Gửi Trưởng Làng,",
  "story.common.outro1": "Dưới sự cai trị ân đức của Đức Vua,\nCông Tước Micalico\nKhâm Sai Hoàng Triều",
  "story.common.outro2": "Bà con đồng bào thuộc địa",

  "story.tut1": "Cầu chúc hải trình bình an cho mọi thần dân dưới Vương Triều.\n\nCác thuyền trinh sát hoàng triều đã xác định quần đảo được giao cho ngươi là một thuộc địa đầy tiềm năng trong khuôn khổ Đoàn Thám Hiểm Hoàng Gia năm 1681. 72 thuộc địa như vậy đã được thiết lập thành công nhờ nỗ lực kiên cường của các chiến binh Mèo Móng Vuốt dũng cảm. Dưới sự dẫn dắt nhân từ của Đức Vua, thuộc địa của ngươi có thể trở thành thuộc địa thứ 73 vẻ vang ấy.\n\nCông trình tối quan trọng của ngươi sẽ là Bến Cảng Chính. Không có nó, thuộc địa không thể nào trả nổi nợ nần cho triều đình. Vì vậy ta yêu cầu ngươi hãy chọn một hòn đảo và dựng bến cảng ngay. Hãy tìm nơi có nhiều Gỗ Rừng và Bụi Quả Mọng gần kề.",

  "story.tut2": "Kho bãi đóng vai trò sống còn để bảo toàn giá trị thị trường của hàng cống nộp thuế má. Mỗi kho bãi đều có sức chứa giới hạn. Hãy cẩn thận đừng để kho chứa đầy những thứ phế phẩm vô giá trị. Hãy tập trung tích trữ tài nguyên hữu ích cho Vương Quốc: Gỗ Khúc, Xơ Bông và Quặng Kim Loại.\n\nNhững hàng hóa này mới bảo quản được qua các chuyến hải trình dài ngày và tạo thêm việc làm cho lũ chuột thợ trong các đại công xưởng hoàng triều. Để giảm quãng đường khuân vác, ngươi nên thi công bản vẽ Kho Tổng đính kèm ngay gần Bến Cảng Chính.",

  "story.tut3": "Xin chúc mừng ngươi và các thuộc dân đồng hương. Chiếu theo ủy thác của Đức Vua, ta vinh dự trao bản Hiến Chương Thuộc Địa này cho các ngươi.\n\nNgươi đang dấn thân vào một sứ mệnh xứng đáng với những chú chuột vĩ đại nhất, và toàn thể đồng loại sẽ phải tri ân những cống hiến nhọc nhằn của ngươi. Khi ngươi thuần hóa những vùng đất hoang sơ này và gom đủ sản vật nộp thuế, ngươi đang làm được nhiều hơn bất kỳ chú chuột nào trước đây. Bằng những giọt mồ hôi của mình, ngươi bảo đảm phương kế sinh nhai an toàn cho những chú chuột chăm chỉ làm ăn.\n\nHãy phụng sự Đức Vua tận tụy, rồi nền hòa bình thịnh trị của ngài sẽ ngự trị khắp các hòn đảo này.",

  "story.quest.survive": "Kho lương của chúng ta đang cạn kiệt thảm hại. Số lương khô này khó lòng cầm cự quá hai ngày. Con tàu thuộc địa chở thừa mứa vật liệu để dựng bến cảng và kho bãi theo thiết kế của hoàng gia, nhưng cho nhu cầu sống sót của chính chúng ta thì chỉ có vài mẩu vụn thừa thãi.\n\nChúng ta phải tìm ngay nguồn thức ăn để sinh tồn và bằng cách nào đó kiếm đủ hàng nộp cho chuyến tàu thu thuế sắp tới.",

  "story.quest.housing": "Còn nhiều chuyện cấp bách đang chờ Trưởng Làng định đoạt. Nhà ở không phải thứ xa xỉ. Vài chú chuột đã phải dựng lều tạm bợ ngoài trời. Chúng tôi khẩn thiết xin Trưởng Làng hãy lo cho bà con một mái nhà che nắng che mưa. Thuộc địa không thể nào tồn tại nếu phải sống phơi mình trước sương gió bão bùng.\n\nMùa đông ập đến nhiệt độ sẽ giảm xuống thảm hại, và chúng ta không thể chống chọi với giá rét chỉ bằng vài ngọn lửa hồng đâu. Mái nhà ấm cúng là tuyến phòng thủ duy nhất của chúng ta.",

  "title.quest.survive": "Bảo Đảm Nguồn Lương Thực",
  "title.quest.housing": "Thị Trấn Của Riêng Chúng Ta",
  "title.quest.resources": "Mỏ Quặng Dưới Lòng Đất",
  "story.quest.resources": "Nộp thuế cho Hoàng Triều là nghĩa vụ hàng đầu của ngươi. Đa số các thuộc địa trả thuế bằng Quặng. Quặng đồng mang lại giá trị cao nhất, nhưng Than đá lại dồi dào hơn. Những thuộc địa cùng quẫn sẽ phải xuất khẩu cả Gỗ khúc xây dựng. Ngươi nên khôn ngoan chọn con đường không dồn mình vào bước đường cùng.\n\nHãy xây dựng và phân công đủ 2 thợ vào ít nhất 1 Khu Khai Thác Mỏ.",

  "title.quest.pop1": "Tăng Trưởng Dân Số",
  "story.quest.pop1": "Ngươi đã được đồng loại chuột tín nhiệm giao phó trọng trách dẫn dắt thuộc địa. Đây là vinh dự lớn nhất mà một chú chuột có thể đạt được. Hàng ngàn bầy chuột ở đất liền đang tha thiết van nài được chuyển đến sống tại các thuộc địa như của ngươi. Nguyện vọng duy nhất của chúng là được phụng sự Hoàng Triều trên một hòn đảo hoang sơ. Đừng làm chúng thất vọng.\n\nHãy phát triển thuộc địa lên 21 Dân Chuột để bắt đầu đóng thuế thực thụ cho triều đình.",

  "title.quest.pirateattack": "Không Thỏa Hiệp Với Hải Tặc",
  "story.quest.pirateattack": "Đang có tin báo về việc hải tặc đòi tiền chuộc ở vùng biển của ngươi. Trong bất kỳ hoàn cảnh nào, tuyệt đối không được nhượng bộ hay thậm chí nghĩ tới việc chấp thuận yêu sách tống tiền của chúng.\n\nNếu thuộc địa của ngươi còn sống sót, hãy báo cáo lại các thủ đoạn tống tiền của lũ hải tặc.",

  # Cockroach Quest
  "story.quest.mousetraps": "Gián! Chúng đã tràn ngập Kho Tổng của chúng ta! Thậm chí chúng có thể đang ẩn náu trong các kho bãi khác nữa. Lũ bẩn thỉu đó đang ngốn gần 2 phần Thức Ăn mỗi phút!\n\nMột nhóm trong chúng tôi đã nghĩ ra cách cải tiến Xưởng Xẻ Gỗ để làm Bẫy. Hãy chuyển công thức sản xuất tại bất kỳ Xưởng Xẻ Gỗ nào. Tích trữ 13 Bẫy Sâu Bọ sẽ đủ để dập tắt mối hiểm họa này.",
  "story.quest.mousetraps.failure": "Đáng tiếc là chúng ta không kịp chế tạo đủ bẫy đúng hạn. Nạn sâu bọ đã lan sang cả các cơ sở sản xuất!\n\nChúng tôi sẽ cố gắng dọn dẹp hết sức trong vài ngày tới...",
  "title.quest.pestcontrol": "Diệt Trừ Sâu Bọ",
  "quest.resolved": "Biến cố đã được giải quyết.",
  "quest.failed": "Biến cố không được giải quyết.",
  "story.quest.mousetraps.success": "Nhờ số bẫy được cung ứng kịp thời, chúng ta đã kiểm soát được bầy sâu bọ! Cảm ơn Trưởng Làng đã tương trợ kịp thời!",

  "unlockPanel.newBlueprint": "Đã Nhận Bản Vẽ Kỹ Thuật Mới",
  "unlockPanel.newRecipe": "Công Thức Mới",
  "unlockpanel.questTechnology": "Bản Vẽ Phần Thưởng Nhiệm Vụ",
  "mission.lastsUntilResolved": "Kéo dài cho tới khi giải quyết xong",
  "mission.objective": "Mục Tiêu",
  "mission.reward": "Phần Thưởng",
  "mission.ifNotResolvedIn": "Nếu không giải quyết trong vòng",

  # Stats Categories
  "statCategory.extracted": "Khai Thác",
  "statCategory.produced": "Sản Xuất Tại Xưởng",
  "statCategory.usedByIndustry": "Dùng Cho Công Nghiệp",
  "statCategory.construction": "Thi Công Xây Dựng",
  "statCategory.consumption": "Tiêu Thụ Đời Sống",
  "statCategory.trade": "Giao Thương & Xuất Khẩu",
  "statCategory.other": "Sự Kiện Đặc Biệt",

  # Rewards
  "reward.mechanical": "Máy Móc Rỉ Sét",
  "reward.food": "Lương Khô Cũ",
  "reward.materialWood": "Gỗ Phế Liệu",
  "reward.materialStone": "Đá Phế Liệu",
  "reward.fuel": "Than Cũ",
  "reward.metals": "Kim Loại Phế Liệu",
  "reward.whisker": "Người Đi Lậu Vé Phát Hiện Được",
  "reward.farmSupplies": "Dụng Cụ Nông Nghiệp",
  "reward.medicine": "Hòm Thuốc Cũ",
  "reward.taxcredit": "Tín Dụng Thuế",

  # Demo / EA / Wishlist
  "demo.fullgame": "Không Có Sẵn Trong Bản Thử Nghiệm",
  "demo.wishlistupsell": "Thêm Whiskerwood Vào Danh Sách Ước Ngay",
  "demo.wishlistcalltoaction": "Thêm vào danh sách ước",
  "demo.demologo": "Bản Xem Trước",
  "welcome.title": "Trò chơi vẫn đang trong quá trình phát triển.",
  "welcome.eawarning": "Chào mừng bạn đến với phiên bản Early Access của Whiskerwood! Chúng tôi rất vui mừng được chia sẻ trò chơi này cùng bạn, và vô cùng hào hứng lắng nghe mọi ý kiến đóng góp từ bạn. Trong suốt giai đoạn Early Access, chúng tôi sẽ liên tục bổ sung nội dung, tính năng mới, sửa lỗi, cân bằng lối chơi và không ngừng nỗ lực hoàn thiện game dựa trên phản hồi của cộng đồng người chơi. Cảm ơn sự ủng hộ nhiệt tình của bạn trong hành trình xây dựng Whiskerwood thành trải nghiệm tuyệt vời nhất!",
  "welcome.byline": "Daniel,\nLập trình viên",
  "welcome.verb": "Tiếp Tục",

  # 9. Modifiers & Status Moodlets (50 items)
  "mod.nosleep": "Thiếu Ngủ",
  "mod.hunger": "Đói Bụng",
  "mod.starvation": "Đói Lả",
  "mod.injury.illness": "Mắc Bệnh",
  "mod.injury.wound": "Bị Thương",
  "mod.injury.extremeillness": "Bệnh Cực Nặng",
  "mod.chilly": "Hơi Lạnh",
  "mod.cold": "Rét Buốt",
  "mod.Freezing": "Chết Cóng",
  "mod.bathed": "Tắm Nước Nóng",
  "mod.matchingGuildEmployer": "Đúng Nghề Bang Hội",
  "mod.rawFoodComplaint": "Ăn Đồ Sống",
  "mod.newarrival": "Chuột Mới Đến",
  "mod.statueIntimidation": "Uy Áp Tượng Đá",
  "mod.statueIntimidation2": "Khiếp Sợ Tột Cùng",
  "mod.engineerPassive": "Hội Thợ Máy",
  "mod.explorersPassive": "Hội Thám Hiểm",
  "mod.minersPassive": "Hội Thợ Mỏ",
  "mod.trait.swift": "Nhanh Nhẹn",
  "mod.trait.strongshoulders": "Đôi Vai Vạm Vỡ",
  "mod.trait.scientist": "Say Mê Nghiên Cứu",
  "mod.lightpollution": "Khói Bụi Mờ Mịt",
  "mod.heavypollution": "Ô Nhiễm Ngột Ngạt",

  # Modifier descriptions
  "mod.desc.nosleep": "Đêm qua không được ngả lưng trong một mái ấm đàng hoàng",
  "mod.desc.hunger": "Cả ngày qua không kiếm được miếng ăn",
  "mod.desc.starvation": "Sẽ chết sớm nếu không có thức ăn vào bụng!",
  "mod.desc.injury.illness": "Ốm nặng nguy kịch",
  "mod.desc.injury.wound": "Chấn thương thể xác và đang cần điều trị",
  "mod.desc.injury.extremeillness": "Đã cận kề miệng vực tử thần",
  "mod.desc.chilly": "Hơi rét buốt và lạnh cóng bàn chân",
  "mod.desc.cold": "Run rẩy dữ dội và tê dại bàn chân",
  "mod.desc.Freezing": "Lạnh thấu xương chết người. Hãy tìm nơi sưởi ấm ngay lập tức!",
  "mod.desc.bathed": "Tận hưởng những giây phút thư thái tại nhà tắm hơi",
  "mod.desc.matchingGuildEmployer": "Bé chuột đang làm công việc đúng với chuyên môn của bang hội",
  "mod.desc.rawFoodComplaint": "Phải gặm nguyên liệu thô sống là nỗi sỉ nhục với Hội Nông Dân",
  "mod.desc.newarrival": "Bé chuột mới chân ướt chân ráo tới thuộc địa và tràn ngập niềm lạc quan",
  "mod.desc.statueIntimidation": "Cảm thấy bị uy hiếp trước tượng Quý Tộc Mèo gần đó",
  "mod.desc.statueIntimidation2": "Cực kỳ khiếp sợ trước tượng Quý Tộc Mèo gần đó",
  "mod.desc.engineerPassive": "Bà con chuột Hội Thợ Máy là những thợ thuyền làm việc vô cùng năng suất",
  "mod.desc.explorersPassive": "Bà con chuột Hội Thám Hiểm di chuyển nhanh nhẹn trên cả đường sá lẫn địa hình hoang dã",
  "mod.desc.minersPassive": "Bà con chuột Hội Thợ Mỏ vạm vỡ khỏe mạnh và có thể khuân vác thêm tài nguyên",
  "mod.desc.trait.swift": "Chú chuột này di chuyển nhanh nhẹn phi thường",
  "mod.desc.trait.strongshoulders": "Chú chuột này khỏe mạnh phi thường",
  "mod.desc.trait.scientist": "Chú chuột này rất tinh thông trong việc Nghiên Cứu",
  "mod.desc.lightpollution": "Không khí ô nhiễm khói bụi",
  "mod.desc.heavypollution": "Ho sặc sụa giữa màn khói bụi ô nhiễm nặng nề",

  # 10. Messages, Events & Quest Goals (60 items)
  "message.taxshiparrived": "Tàu thu thuế đã cập bến",
  "message.firstWhiskersArrived": "Bầy chuột của bạn đã cập bến",
  "message.firstSuppliesArrived": "Hàng tiếp tế của bạn đã cập bến",
  "message.whiskerShipArrived": "Tàu chở dân chuột đã cập bến",
  "message.weaselSupplyShipArived": "Tàu tiếp tế đã cập bến",
  "message.piratesArrived": "Hải tặc đã gửi tối hậu thư đòi tiếp tế!",
  "message.daybegins": "Ngày <0> bắt đầu",
  "message.shipDepartingSoon": "Tàu neo đậu tại bến sắp sửa rời cảng!",
  "message.decidingRewards": "Phái đoàn Quý Tộc Mèo sẽ sớm diện kiến bạn",
  "message.policiesUnlocked": "Đã Mở Khóa Chính Sách",
  "message.policySlotGained": "Đã Lập Văn Phòng - Nhận Thêm Ô Chính Sách",
  "message.policySlotLost": "Văn Phòng Bị Phá - Mất Ô Chính Sách",
  "message.dayended": "Ngày <0> đã kết thúc",
  "message.dayendedGeneric": "Ngày dài đã khép lại",
  "message.messages": "Bảng Tin",
  "counter.lasts": "Kéo dài",
  "eventType.message": "Tin Nhắn",
  "eventType.decision": "Quyết Định",
  "eventType.request": "Nhiệm Vụ Mới",
  "event.dockedShip": "Tàu Cập Bến",
  "eventType.tutorial": "Cố Vấn",
  "eventType.deaths": "Bản Cáo Phó",
  "eventType.questComplete": "Nhiệm Vụ Đã Sẵn Sàng",
  "eventType.missionexpiration": "Nhiệm Vụ Đã Hết Hạn",

  # Quest Goals
  "questgoal.population": "Dân Số",
  "questgoal.buildingCount": "Đã xây <0>",
  "questgoal.production": "Sản xuất <0>",
  "questgoal.deliverResources": "Giao nộp <0>",
  "questgoal.earnInfluence": "Lòng Dân Tích Lũy",
  "questgoal.housingSpace": "Chỗ Ở",
  "questgoal.onedayproduction": "Sản xuất <0> hôm nay",
  "questgoal.nodes.trees": "Cây đã đốn hạ",
  "questgoal.nodes.berries": "Quả mọng đã hái",
  "questgoal.nodes.fish": "Cá đã đánh bắt",
  "questgoal.workers": "<0> công nhân",
  "questgoal.farmed": "<0> từ đồng ruộng",
  "quest.generic": "Nhiệm Vụ",

  # Machine & Structure Status
  "fluidcontrol.limit": "Cho phép dẫn dòng nếu bên Cửa Vào vượt mức:",
  "launcher.launchCost": "Chi phí bắn:",
  "launcher.noDestination": "Chưa Gán Điểm Đến!",
  "construction.instant": "Xây Tức Thì",
  "construction.free": "Thi Công Miễn Phí",
  "slotdecorative.lamp": "Đèn Lồng",
  "slotdecorative.torch": "Đuốc Lửa",
  "slotdecoractive.ropefence": "Lan Can Dây Thừng",
  "slotdecorative.cobblefence": "Hàng Rào Đá Cuội",
  "slotdecorative.privacyfence": "Hàng Rào Kín Đáo",
  "slotdecorative.barrels": "Thùng Gỗ",
  "slotdecorative.crates": "Hòm Hàng",
  "slotdecorative.bench": "Ghế Băng",
  "slotdecorative.planter": "Chậu Cây Cảnh",
  "slotdecorative.onewaygate": "Cổng Một Chiều",
  "slotdecorative.stonerailing": "Lan Can Đá",
  "agent.speed": "Tốc Độ Di Chuyển",
  "agent.efficiency": "Tốc Độ Làm Việc",
  "agent.strength": "Sức Khuân Vác",
  "steamengine.idle": "Nghỉ",
  "steamengine.powered": "Đang Cung Cấp Năng Lượng",
  "structuretemperature.freezing": "Giá Rét Nguy Cấp",
  "structuretemperature.freezing.desc": "Giá rét nguy hiểm cho công nhân và gây hao tổn nặng nề cho máy móc công nghiệp."
}

def apply_phase6a():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    applied_count = 0
    missing = []
    # Phase 6A covers first 335 items
    for item in data[:335]:
        key = item.get('key')
        if key in T_6A:
            item['target_vi'] = T_6A[key]
            applied_count += 1
        else:
            missing.append((item['id'], key, item.get('source_en')))

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Applied translation to {applied_count} / 335 items in Phase 6A!")
    if missing:
        print(f"Missing {len(missing)} items in Phase 6A:")
        for m in missing[:20]:
            print(" ", m)
    else:
        print("All 335 Phase 6A items translated 100%!")

if __name__ == "__main__":
    apply_phase6a()
