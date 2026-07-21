import json

def analyze_skill_gap(resume_data, jd_data):
    resume_skills={s.lower() for s in resume_data.get("skills",[])}
    required={s.lower() for s in jd_data.get("required_skills",[])}
    critical={s.lower() for s in jd_data.get("critical_skills",[])}
    optional={s.lower() for s in jd_data.get("optional_skills",[])}

    matched=sorted(required & resume_skills)
    missing=sorted(required-resume_skills)
    critical_missing=sorted(critical-resume_skills)
    optional_missing=sorted(optional-resume_skills)

    skill_match=round(len(matched)/len(required)*100,2) if required else 100
    critical_match=round((len(critical)-len(critical_missing))/len(critical)*100,2) if critical else 100

    return {
      "matched_skills":matched,
      "missing_skills":missing,
      "critical_missing_skills":critical_missing,
      "optional_missing_skills":optional_missing,
      "skills_to_learn_first":critical_missing+[x for x in missing if x not in critical_missing],
      "features":{
        "skill_match_percentage":skill_match,
        "critical_skill_match_percentage":critical_match,
        "missing_skills_count":len(missing),
        "critical_missing_skills_count":len(critical_missing),
        "project_relevance_score":resume_data.get("project_relevance_score",80),
        "certification_relevance_score":min(100,len(resume_data.get("certifications",[]))*20),
        "internship_relevance_score":min(100,len(resume_data.get("internships",[]))*50),
        "resume_completeness_score":resume_data.get("resume_completeness",0),
        "keyword_match_score":round(len(set(jd_data.get("keywords",[])) & resume_skills)/max(1,len(jd_data.get("keywords",[])))*100,2),
        "role_category_match_score":100 if resume_data.get("resume_category","").lower()==jd_data.get("role_category","").lower() else 60,
        "education_score":90 if resume_data.get("education") else 40
      }
    }
