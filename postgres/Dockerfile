FROM postgres
ENV POSTGRES_PASSWORD ${POSTGRES_PASS}
ENV POSTGRES_DB ${POSTGRES_DATA}
COPY article_and_comment_table.sql /docker-entrypoint-initdb.d/article_and_comment_table.sql
EXPOSE 5432
