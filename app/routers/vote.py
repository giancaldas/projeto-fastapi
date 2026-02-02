from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, database, oauth2


router = APIRouter(tags=["Vote"])


@router.post("/posts/{post_id}/votes", status_code=status.HTTP_201_CREATED)
def create_vote(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    found_vote = (
        db.query(models.Vote)
        .filter(models.Vote.post_id == post_id, models.Vote.user_id == current_user.id)
        .first()
    )
    if found_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} has already voted on post {post_id}",
        )

    new_vote = models.Vote(post_id=post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "successfully added vote"}


@router.delete("/posts/{post_id}/votes", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist"
        )
    vote_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/votes/{vote_id}", status_code=status.HTTP_200_OK)
def get_votes(
    vote_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    votes = (
        db.query(func.count(models.Vote.post_id))
        .filter(models.Vote.post_id == vote_id)
        .scalar()
    )
    return {"post_id": vote_id, "total_votes": votes}
