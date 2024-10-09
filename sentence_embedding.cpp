#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 
#include <string>
#include <vector>

namespace py = pybind11;

class SentenceEmbedding {
public:
    SentenceEmbedding(const std::string& sentence, const std::vector<float>& embeddings)
        : sentence_(sentence), embeddings_(embeddings) {}

    std::string get_sentence() const {
        return sentence_;
    }

    py::array_t<float> get_embeddings() const {
        return py::array_t<float>(embeddings_.size(), embeddings_.data());
    }

    py::tuple get_most_similar(const std::vector<SentenceEmbedding>& embeddings_list, const std::string& metric = "cosine") const {
        int most_similar_id = -1;
        float best_score = (metric == "euclidean") ? std::numeric_limits<float>::max() : -std::numeric_limits<float>::max();  // Start with maximum/minimum score based on the metric

        for (size_t i = 0; i < embeddings_list.size(); ++i) {
            const auto& other_embedding = embeddings_list[i].embeddings_;


            float score = 0.0f;
            if (metric == "euclidean") {
                // Calculate the Euclidean distance
                float distance=0.0f;
                for (size_t j = 0; j < embeddings_.size(); ++j) {
                    float diff = embeddings_[j] - other_embedding[j];
                    distance += diff * diff; 
                }
                distance = std::sqrt(distance);
                score = distance;
                if (distance < best_score) {
                    best_score = distance;
                    most_similar_id = static_cast<int>(i);
                }
            } else if (metric == "cosine") {
                // Calculate cosine similarity
                float dot_product = 0.0f;
                float norm_a = 0.0f;
                float norm_b = 0.0f;
                for (size_t j = 0; j < embeddings_.size(); ++j) {
                    dot_product += embeddings_[j] * other_embedding[j];
                    norm_a += embeddings_[j] * embeddings_[j];
                    norm_b += other_embedding[j] * other_embedding[j];
                }
                norm_a = std::sqrt(norm_a);
                norm_b = std::sqrt(norm_b);
                score = (norm_a != 0 && norm_b != 0) ? (dot_product / (norm_a * norm_b)) : 0.0f;

                if (score > best_score) {
                    best_score = score;
                    most_similar_id = static_cast<int>(i);
                }
            }
        }

        return py::make_tuple(most_similar_id, best_score);
    }
private:
    std::string sentence_;
    std::vector<float> embeddings_;
};

PYBIND11_MODULE(sentence_embedding, m) {
    py::class_<SentenceEmbedding>(m, "SentenceEmbedding")
        .def(py::init<const std::string&, const std::vector<float>&>())
        .def("get_sentence", &SentenceEmbedding::get_sentence)
        .def("get_embeddings", &SentenceEmbedding::get_embeddings)
        .def("get_most_similar", &SentenceEmbedding::get_most_similar);
}
